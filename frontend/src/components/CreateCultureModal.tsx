import React, { useEffect, useState, useContext } from "react";
import Modal from "react-modal";
import API from "../API";
import { ICulture } from "./IFarmer";
import { OptionsContext } from "../context/OptionsContext";

interface ICreateCultureModalProps {
    isEdit: boolean;
    culture?: ICulture
    modalIsOpen: boolean;
    setModalIsOpen: React.Dispatch<React.SetStateAction<boolean>>;
    refreshKey2: number;
    setRefreshKey2: React.Dispatch<React.SetStateAction<number>>;
}

export default function CreateCultureModal({ isEdit, culture, modalIsOpen, setModalIsOpen, refreshKey2, setRefreshKey2 }: ICreateCultureModalProps) {
    const [name, setName] = useState<string>("");
    const { selectedOption, refreshKey, setRefreshKey } = useContext(OptionsContext);

    useEffect(() => {
        if (isEdit && culture) {
            setName(culture.name);
        } else {
            setName("");
        }
    }, [isEdit, culture]);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        const newCulture = { name };
        if (isEdit) {
            const response = await API.put(`/api/v1/farmer/${selectedOption}/culture`, newCulture);

            if (response.status === 200) {
                setModalIsOpen(false);
                setRefreshKey(refreshKey + 1);
                setRefreshKey2(refreshKey2 + 1);
            } else {
                alert("Error editing culture!")
            }
        } else {
            const response = await API.post(`/api/v1/farmer/${selectedOption}/culture`, newCulture);

            if (response.status === 201) {
                setModalIsOpen(false);
                setRefreshKey(refreshKey + 1);
                setRefreshKey2(refreshKey2 + 1);
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