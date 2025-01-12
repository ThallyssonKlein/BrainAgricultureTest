import React, { useEffect, useState, useContext } from "react";
import Modal from "react-modal";
import API from "../API";
import { ICulture } from "./IFarmer";
import { OptionsContext } from "../context/OptionsContext";
import { TablesContext } from "../context/TablesContext";
import { ApiResponse } from "apisauce";

interface ICreateCultureModalProps {
    isEdit: boolean;
    modalIsOpen: boolean;
    setModalIsOpen: React.Dispatch<React.SetStateAction<boolean>>;
    setRefreshCropModal: React.Dispatch<React.SetStateAction<number>>;
    selectedCultureObject: ICulture | null | undefined;
    setCultures: React.Dispatch<React.SetStateAction<ICulture[] | null>>;
}

export default function CultureModal({ isEdit, modalIsOpen, setModalIsOpen, setRefreshCropModal, selectedCultureObject, setCultures }: ICreateCultureModalProps) {
    const [name, setName] = useState<string>("");
    const { selectedOption } = useContext(OptionsContext);
    const { selectedFarmId, setCrops, setFarms, farms } = useContext(TablesContext);

    useEffect(() => {
        if (isEdit && selectedCultureObject) {
            setName(selectedCultureObject.name);
        } else {
            setName("");
        }
    }, [isEdit, selectedCultureObject]);

    const refreshCultures = (response: ApiResponse<unknown, unknown>) => {
        const selectedFarm = farms.find(farm => farm.id === selectedFarmId);
        const createdCulture = response.data as ICulture
        if (selectedFarm) {
            setFarms(prevFarms => prevFarms.map(farm => 
                farm.id === selectedFarmId 
                ? { ...farm, crops: farm.crops?.map(crop => {
                    if (crop.culture?.id === createdCulture.id) {
                        crop.culture = createdCulture;
                    }

                    return crop;
                }) || [] } 
                : farm
            ));
        } else {
            setCrops((previousCrops) => previousCrops.map(crop => {
                if (crop.culture?.id === createdCulture.id) {
                    crop.culture = createdCulture;
                }

                return crop;
            })
            );
        }
        setModalIsOpen(false);
        setRefreshCropModal(previous => previous + 1);
    }
    
    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        let newCulture: { name: string; old_name?: string } = { name };
        if (isEdit) {
            newCulture = { ...newCulture, old_name: selectedCultureObject?.name };
            const response = await API.put(`/api/v1/culture/${selectedCultureObject?.id}`, newCulture);
            const createdCulture = response.data as ICulture
            if (response.status === 200) {
                refreshCultures(response);
                setCultures(prevState => {
                    if (prevState && prevState.length > 0) {
                        const culture = prevState.find(culture => culture.id === createdCulture.id);
                        const arrayWithoutCulture = prevState.filter(culture => culture.id !== createdCulture.id);
                        return [...arrayWithoutCulture, culture as ICulture];
                    }
                    return prevState;
                });        
            } else if (response.status === 409) {
                alert("Cultura já existe!")
            } else {
                alert("Erro editando cultura!")
            }
        } else {
            const response = await API.post(`/api/v1/farmer/${selectedOption.id}/culture`, newCulture);

            if (response.status === 201) {
                refreshCultures(response);
                setCultures(prevState => {
                    if (prevState && prevState.length > 0) {
                        return [...prevState, response.data as ICulture];
                    }
                    return prevState;
                })
            } else if (response.status === 409) {
                alert("Cultura já existe!")
            } else {
                alert("Erro criando cultura!")
            }
        }
    };

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
            <h2>{isEdit ? "Editar Cultura" : "Criar Cultura"}</h2>
            <form onSubmit={handleSubmit}>
                <div style={{ marginBottom: '50px' }}>
                    <label>Name: </label>
                    <input type="text" value={name} onChange={(e) => setName(e.target.value)} required />
                </div>
                <button 
                    type="submit"
                    style={{
                        position: 'absolute',
                        bottom: '10px',
                        right: '20px',
                        marginLeft: '30px',
                        cursor: 'pointer',
                    }}
                >{isEdit ? "Atualizar" : "Salvar"}</button>
            </form>
    </Modal>
    )
}