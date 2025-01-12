import React, { useEffect, useState, useContext } from "react";
import Modal from "react-modal";
import API from "../API";
import { ICrop, ICulture } from "./IFarmer";
import { OptionsContext } from "../context/OptionsContext";
import { TablesContext } from "../context/TablesContext";

interface ICreateCultureModalProps {
    isEdit: boolean;
    modalIsOpen: boolean;
    setModalIsOpen: React.Dispatch<React.SetStateAction<boolean>>;
    setRefreshKey2: React.Dispatch<React.SetStateAction<number>>;
    selectedCultureObject: ICulture | null;
    selectedCrop: ICrop | null;
}

export default function CultureModal({ isEdit, modalIsOpen, setModalIsOpen, setRefreshKey2, selectedCultureObject, selectedCrop }: ICreateCultureModalProps) {
    const [name, setName] = useState<string>("");
    const { selectedOption, setRefreshKey } = useContext(OptionsContext);
    const { setSelectedFarm, selectedFarm, setCrops } = useContext(TablesContext);

    useEffect(() => {
        if (isEdit && selectedCultureObject) {
            setName(selectedCultureObject.name);
        } else {
            setName("");
        }
    }, [isEdit, selectedCultureObject]);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        const newCulture = { name };
        if (isEdit) {
            const response = await API.put(`/api/v1/culture/${selectedCultureObject?.id}`, newCulture);

            if (response.status === 200) {
                const updatedResponseData = response.data as ICulture;

                if (selectedFarm && setSelectedFarm) {
                    const updatedFarm = selectedFarm;
                    updatedFarm.crops = updatedFarm.crops?.map(crop => {
                        if (crop.culture_id === updatedResponseData.id || crop.culture?.id === updatedResponseData.id) {
                            return {
                                ...crop,
                                culture: updatedResponseData,
                                culture_id: updatedResponseData.id,
                                culture_name: updatedResponseData.name
                            };
                        }
                        return crop;
                    });
                    setSelectedFarm(
                        updatedFarm
                    )
                } else {
                    setCrops((prevState: ICrop[]) => {
                        return prevState?.map((crop: ICrop) => {
                            if (crop.culture_id === updatedResponseData.id || crop.culture?.id === updatedResponseData.id) {
                                return {
                                    ...crop,
                                    culture: updatedResponseData,
                                    culture_id: updatedResponseData.id,
                                    culture_name: updatedResponseData.name
                                };
                            }
                            return crop;
                        });
                    });
                }

                setModalIsOpen(false);
                setRefreshKey(previous => previous + 1);
                setRefreshKey2(previous => previous + 1);
            } else {
                alert("Error editing culture!")
            }
        } else {
            const response = await API.post(`/api/v1/farmer/${selectedOption}/culture`, newCulture);

            if (response.status === 201) {
                setModalIsOpen(false);
                setRefreshKey(previous => previous + 1);
                setRefreshKey2(previous => previous + 1);
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