import React, { useState, useContext, useEffect } from "react";
import Modal from "react-modal";
import { OptionsContext } from "../context/OptionsContext";
import API from "../API";
import CultureModal from "./CultureModal";
import { ICrop, ICulture, IFarm } from "./IFarmer";
import { CropModalContext } from "../context/CropModalContext";
import { TablesContext } from "../context/TablesContext";

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

    const refreshTablesAndCharts = () => {
        const selectedFarm = farms.find(farm => farm.id === selectedFarmId);
        if (selectedFarm) {
            setFarms(prevFarms => prevFarms.map(farm => 
                farm.id === selectedFarmId 
                ? { ...farm, crops: farm.crops?.map(crops => {
                    if (crops.id === selectedCrop?.id) {
                        crops.date = date;
                    }
                    return crops;
                }) || [] } 
                : farm
            ));
        } else {
            setCrops((previousCrops) => previousCrops.map(crop => {
                if (crop.id === selectedCrop?.id) {
                    crop.date = date;
                }
                return crop;
            })
          );
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
            alert("Select one culture");
            return;
        }

        const newCrop = { date, culture: { id: selectedCulture } };
        if (isEdit) {
            const response = await API.put(`/api/v1/crop/${selectedCrop?.id}`, newCrop);

            if (response.status === 200) {
                setSavedSuccessFullyMessage(true);
                setTimeout(() => {
                    setSavedSuccessFullyMessage(false);
                }, 2000);
            } else {
                setSavedWithErrorMessage(true);
                setTimeout(() => {
                    setSavedWithErrorMessage(false);
                }, 2000);

                refreshTablesAndCharts();
            }
        } else {
            const response = await API.post(`/api/v1/farm/${selectedOption}/crop`, newCrop);

            if (response.status === 201) {
                setSavedSuccessFullyMessage(true);
                setTimeout(() => {
                    setSavedSuccessFullyMessage(false);
                }, 2000);
                setDate("");
                setSelectedCulture(null);

                refreshTablesAndCharts();
            } else {
                setSavedWithErrorMessage(true);
                setTimeout(() => {
                    setSavedWithErrorMessage(false);
                }, 2000);
            }
        }
    };

    useEffect(() => {
        (async () => {
            const response = await API.get(`/api/v1/farmer/${selectedOption}/culture`);
            
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

        const userResponse = window.confirm("Do you want to proceed?");
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
            alert("Culture is being used in a crop, cannot delete!");
        } else {
            alert("Error deleting!");
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
            <h2>{isEdit ? "Edit Crop and Cultures" : "Create Crop and Cultures"}</h2>
            <form onSubmit={handleSubmit}>
                <div>
                    <label>Date: </label>
                    <input type="date" value={date} onChange={(e) => setDate(e.target.value)} required />
                </div>
                <h1>Select One Culture or Create It</h1>
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
                                        style={{ cursor: 'pointer', background: selectedCulture === culture.id ? 'red' : 'white' }}
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
                                            >Edit</button>
                                        </td>
                                        <td>
                                            <button onClick={(event) => handleDeleteCulture(culture.id)}>Delete</button>
                                        </td>
                                    </tr>                  
                                ))
                            }
                            </tbody>
                        </table>
                        <div style={{ display: 'flex', flexDirection: 'row', alignItems: 'center' }}>
                            <button 
                                style={{flex: 1}}
                                onClick={() => {
                                    setIsEditCulture(false);
                                    setCultureModalIsOpen(true);
                                }}
                            >Create Culture</button>
                        </div>
                    </div>
                    : "Loading cultures..."                  
                }
                <button type="submit">{isEdit ? "Update" : "Save"}</button>
                {savedSuccessFullyMessage && <p>Saved successfully!</p>}
                {savedWithErrorMessage && <p>Something went wrong!</p>}
            </form>
    </Modal>
    )
}