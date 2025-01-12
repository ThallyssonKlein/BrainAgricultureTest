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
        setCultures(prevState => {
            return prevState ? prevState.filter(culture => culture.id !== createdCulture.id) : null;
        });
        setModalIsOpen(false);
        setRefreshCropModal(previous => previous + 1);
    }
    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        const newCulture = { name };
        if (isEdit) {
            const response = await API.put(`/api/v1/culture/${selectedCultureObject?.id}`, newCulture);

            if (response.status === 200) {
                refreshCultures(response);
            } else {
                alert("Error editing culture!")
            }
        } else {
            const response = await API.post(`/api/v1/farmer/${selectedOption}/culture`, newCulture);

            if (response.status === 201) {
                refreshCultures(response);
            } else {
                alert("Error creating culture!")
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
            <h2>{isEdit ? "Edit Culture" : "Create Culture"}</h2>
            <form onSubmit={handleSubmit}>
                <div>
                    <label>Name: </label>
                    <input type="text" value={name} onChange={(e) => setName(e.target.value)} required />
                </div>
                <button type="submit">{isEdit ? "Update" : "Save"}</button>
            </form>
    </Modal>
    )
}