import React, { useState, useContext, useEffect } from "react";
import Modal from "react-modal";
import { FarmModalContext } from "../context/FarmModalContext";
import { OptionsContext } from "../context/OptionsContext";
import API from "../API";

export default function CreateFarmModal() {
    const [vegetationArea, setVegetationArea] = useState<number>(0);
    const [state, setState] = useState<string>("");
    const [name, setName] = useState<string>("");
    const [arableArea, setArableArea] = useState<number>(0);
    const [totalArea, setTotalArea] = useState<number>(0);
    const [city, setCity] = useState<string>("");
    const { modalIsOpen, setModalIsOpen, isEdit } = useContext(FarmModalContext);
    const { selectedOption } = useContext(OptionsContext);
    const [savedSuccessFullyMessage, setSavedSuccessFullyMessage] = useState(false);
    const [savedWithErrorMessage, setSavedWithErrorMessage] = useState(false);

    useEffect(() => {
        if (isEdit && selectedOption) {
            setVegetationArea(selectedOption.vegetation_area);
            setState(selectedOption.state);
            setName(selectedOption.name);
            setArableArea(selectedOption.arable_area);
            setTotalArea(selectedOption.total_area);
            setCity(selectedOption.city);
        } else {
            setVegetationArea(0);
            setState("");
            setName("");
            setArableArea(0);
            setTotalArea(0);
            setCity("");
        }
    }, [isEdit, selectedOption]);

    useEffect(() => {
        console.log("abriu a modal")
    }, [modalIsOpen])

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        const newFarm = { vegetationArea, state, name, arableArea, totalArea, city, id: selectedOption?.id };
        if (isEdit) {
            const response = await API.put(`/api/v1/farm/${selectedOption}`, newFarm);

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
            }
        } else {
            const response = await API.post("/api/v1/farm", newFarm);

            if (response.status === 201) {
                setSavedSuccessFullyMessage(true);
                setTimeout(() => {
                    setSavedSuccessFullyMessage(false);
                }, 2000);
                setVegetationArea(0);
                setState("");
                setName("");
                setArableArea(0);
                setTotalArea(0);
                setCity("");
            } else {
                setSavedWithErrorMessage(true);
                setTimeout(() => {
                    setSavedWithErrorMessage(false);
                }, 2000);
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
            <h2>{isEdit ? "Edit Farm" : "Create Farm"}</h2>
            <form onSubmit={handleSubmit}>
                <div>
                    <label>vegetationArea</label>
                    <input type="number" value={vegetationArea} onChange={(e) => setVegetationArea(Number(e.target.value))} required />
                </div>
                <div>
                    <label>State</label>
                    <input type="text" value={state} onChange={(e) => setState(e.target.value)} required />
                </div>
                <div>
                    <label>Name</label>
                    <input type="text" value={name} onChange={(e) => setName(e.target.value)} required />
                </div>
                <div>
                    <label>arableArea</label>
                    <input type="number" value={arableArea} onChange={(e) => setArableArea(Number(e.target.value))} required />
                </div>
                <div>
                    <label>totalArea</label>
                    <input type="number" value={totalArea} onChange={(e) => setTotalArea(Number(e.target.value))} required />
                </div>
                <div>
                    <label>City</label>
                    <input type="text" value={city} onChange={(e) => setCity(e.target.value)} required />
                </div>
                <button type="submit">{isEdit ? "Update" : "Save"}</button>
                {savedSuccessFullyMessage && <p>Saved successfully!</p>}
                {savedWithErrorMessage && <p>Something went wrong!</p>}
            </form>
    </Modal>
    )
}