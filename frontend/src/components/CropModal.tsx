import React, { useState, useContext, useEffect } from "react";
import Modal from "react-modal";
import { OptionsContext } from "../context/OptionsContext";
import API from "../API";
import CultureModal from "./CultureModal";
import { ICrop, ICulture, IFarm } from "./IFarmer";
import { CropModalContext } from "../context/CropModalContext";
import { TablesContext } from "../context/TablesContext";
import { ApiResponse } from "apisauce";
import messageTranslations from "../messageTranslations"

interface ICreateCropModalProps {
    selectedCrop?: ICrop | null;
}

export default function CropModal({ selectedCrop }: ICreateCropModalProps) {
    const [date, setDate] = useState<string>("");
    const { modalIsOpen, setModalIsOpen, isEdit } = useContext(CropModalContext);
    const { selectedOption, setRefreshCharts } = useContext(OptionsContext);
    const [savedSuccessFullyMessage, setSavedSuccessFullyMessage] = useState(false);
    const [savedWithErrorMessage, setSavedWithErrorMessage] = useState(false);
    const [isEditCulture, setIsEditCulture] = useState(false);
    const [cultureModalIsOpen, setCultureModalIsOpen] = useState(false);
    const [cultures, setCultures] = useState<ICulture[] | null>([]);
    const [selectedCulture, setSelectedCulture] = useState<number | null | undefined>(null);
    const [refreshCropModal, setRefreshCropModal] = useState(0);
    const { setCrops, farms, selectedFarmId, setFarms } = useContext(TablesContext);

    const refreshTablesAndCharts = (isEdit: boolean, response: ApiResponse<unknown, unknown>) => {
        const selectedFarm = farms.find(farm => farm.id === selectedFarmId);
        const createdCrop = response?.data as ICrop;
        if (selectedFarm) {
            if (isEdit) {
                setFarms(prevFarms => prevFarms.map(farm => 
                    farm.id === selectedFarmId 
                    ? { ...farm, crops: farm.crops?.map(crop => {
                        if (crop.id === createdCrop?.id) {
                            crop = createdCrop
                        }
                        return crop;
                    }) || [] } 
                    : farm
                ));
            } else {
                setFarms(prevFarms => prevFarms.map(farm => 
                    farm.id === selectedFarmId 
                    ? { ...farm, crops: farm.crops ? [...farm.crops, createdCrop] : [createdCrop] } 
                    : farm
                ));
            }
        } else {
            if (isEdit) {
                setCrops((previousCrops) => previousCrops.map(crop => {
                    if (crop.id === createdCrop?.id) {
                        crop = createdCrop
                    }
                    return crop;
                }));
            } else {
                setCrops((previousCrops) => previousCrops.concat(createdCrop));
            }
        }
        setRefreshCharts(previos => previos + 1);
    }

    useEffect(() => {
        if (isEdit && selectedOption && selectedCrop) {
            setDate(selectedCrop.date);
        } else {
            setDate("");
            setCultures(null);
        }
    }, [isEdit, selectedOption, selectedCrop]);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();

        if (!selectedCulture) {
            alert("Selecione uma cultura!");
            return;
        }

        if (!date) {
            alert("Selecione uma data!");
            return
        }

        const newCrop = { date, culture: { id: selectedCulture } };
        if (isEdit) {
            const response = await API.put(`/api/v1/crop/${selectedCrop?.id}`, newCrop);

            if (response.status === 200) {
                setSavedSuccessFullyMessage(true);
                setTimeout(() => {
                    setSavedSuccessFullyMessage(false);
                }, 2000);
                refreshTablesAndCharts(isEdit, response);
            } else {
                setSavedWithErrorMessage(true);
                setTimeout(() => {
                    setSavedWithErrorMessage(false);
                }, 2000);
            }
        } else {
            const response = await API.post(`/api/v1/farm/${selectedFarmId}/crop`, newCrop);

            if (response.status === 201) {
                setSavedSuccessFullyMessage(true);
                setTimeout(() => {
                    setSavedSuccessFullyMessage(false);
                }, 2000);
                setDate("");
                setSelectedCulture(null);
                refreshTablesAndCharts(isEdit, response);
            } else {
                if (response.status === 404) {
                    const data = response.data as { message: string };
                    const message = data.message;
                    if (messageTranslations[message]) {
                        alert(messageTranslations[message])
                    }
                }

                setSavedWithErrorMessage(true);
                setTimeout(() => {
                    setSavedWithErrorMessage(false);
                }, 2000);
            }
        }
    };

    useEffect(() => {
        (async () => {
            const response = await API.get(`/api/v1/farmer/${selectedOption.id}/culture`);
            
            if (response.status === 200) {
                setCultures(response.data as ICulture[]);
                if (isEdit) {
                    setSelectedCulture(selectedCrop?.culture?.id ?? undefined);
                }
            }
        })()
    }, [isEdit, refreshCropModal, selectedCrop, selectedOption]);

    const handleDeleteCulture = async (id?: number) => {
        if (!id) {
            return;
        }

        const userResponse = window.confirm("Quer prosseguir?");
        if (userResponse) {
        const response = await API.delete(`/api/v1/culture/${id}`);

        if (response.status === 200){
            const selectedFarm = farms.find(farm => farm.id === selectedFarmId);
            if (selectedFarm) {
                setFarms(prevFarms => prevFarms.map(farm => 
                    farm.id === selectedFarmId 
                    ? { ...farm, crops: farm.crops?.map(crop => {
                        if (crop.culture?.id === id) {
                            crop.culture = null;
                        }

                        return crop;
                    }) || [] } 
                    : farm
                ));
            } else {
                setCrops((previousCrops) => previousCrops.map(crop => {
                    if (crop.culture?.id === id) {
                        crop.culture = null;
                    }

                    return crop;
                })
              );
            }
            setCultures(prevState => {
                return prevState ? prevState.filter(culture => culture.id !== id) : null;
            });
        } else if(response.status === 409){
            alert("Cultura está sendo usada por alguma safra, delete elas primeiro!");
        } else {
            alert("Erro Deletando a Cultura!");
        }
      }
    }

    return (
        <Modal
            isOpen={modalIsOpen}
            onRequestClose={() => setModalIsOpen(false)}
            style={{
                content: {
                    top: '50%',
                    left: '50%',
                    right: 'auto',
                    bottom: 'auto',
                    marginRight: '-50%',
                    transform: 'translate(-50%, -50%)',
                },
            }}
        >
            <CultureModal 
                    isEdit={isEditCulture}
                    modalIsOpen={cultureModalIsOpen}
                    setModalIsOpen={setCultureModalIsOpen}
                    setRefreshCropModal={setRefreshCropModal}
                    selectedCultureObject={cultures?.find(culture => culture.id === selectedCulture)}
                    setCultures={setCultures}
                    />
            <button
                onClick={() => setModalIsOpen(false)}
                style={{
                    position: 'absolute',
                    top: '10px',
                    right: '10px',
                    background: 'transparent',
                    border: 'none',
                    fontSize: '20px',
                    cursor: 'pointer',
                }}
            >
                &times;
            </button>
            <h2>{isEdit ? "Editar Safras e Culturas" : "Criar Safras e Culturas"}</h2>
            <form onSubmit={handleSubmit}>
                <div>
                    <label>Data: </label>
                    <input type="date" value={date} onChange={(e) => setDate(e.target.value)} required />
                </div>
                <h3>Selecione uma Cultura ou Crie Uma</h3>
                {cultures && cultures.length > 0 ? 
                    <div>
                        <table border={1} style={{ width: '100%', marginBottom: '20px', borderCollapse: 'collapse' }}>
                        <thead>
                            <tr>
                                <th style={{ minWidth: '50px', width: '1%' }}>Id</th>
                                <th style={{ minWidth: '100px', width: '10%' }}>Nome da Cultura</th>
                                <th style={{ minWidth: '80px', width: '0.1%' }}>Editar</th>
                                <th style={{ minWidth: '80px', width: '0.1%' }}>Excluir</th>
                            </tr>
                        </thead>
                        <tbody>
                            {
                                cultures.map(culture => (
                                    <tr
                                        key={culture.id}
                                        onClick={() => {
                                            setSelectedCulture(culture.id)
                                        }}
                                        style={{ cursor: 'pointer', background: selectedCulture === culture.id ? '#adacac' : 'white' }}
                                    >
                                        <td>{culture.id}</td>
                                        <td>{culture.name}</td>
                                        <td>
                                        <button
                                            onClick={() => {
                                                setIsEditCulture(true);
                                                setSelectedCulture(null);
                                                setSelectedCulture(culture.id);
                                                setCultureModalIsOpen(true);
                                            }}
                                            >Editar</button>
                                        </td>
                                        <td>
                                            <button onClick={(_event) => handleDeleteCulture(culture.id)}>Excluir</button>
                                        </td>
                                    </tr>                  
                                ))
                            }
                            </tbody>
                        </table>
                        <div style={{ display: 'flex', flexDirection: 'row', alignItems: 'center' }}>
                            <button 
                                style={{flex: 1, marginBottom: 50}}
                                onClick={() => {
                                    setIsEditCulture(false);
                                    setCultureModalIsOpen(true);
                                }}
                            >Criar Cultura</button>
                        </div>
                    </div>
                    : "Loading cultures..."                  
                }
                 <button
                    type="submit"
                    style={{
                        position: 'absolute',
                        bottom: '10px',
                        right: '20px',
                        marginLeft: '30px',
                        cursor: 'pointer',
                    }}
                >
                    {isEdit ? "Atualizar" : "Salvar"}
                </button>
                {savedSuccessFullyMessage && <p>Salvo com sucesso!</p>}
                {savedWithErrorMessage && <p>Algo deu errado!</p>}
            </form>
    </Modal>
    )
}