import React, { useState, useContext, useEffect } from "react";
import Modal from "react-modal";
import { FarmModalContext } from "../context/FarmModalContext";
import { OptionsContext } from "../context/OptionsContext";
import API from "../API";
import { TablesContext } from "../context/TablesContext";
import { IFarm } from "./IFarmer";

export default function FarmModal() {
    const [vegetationArea, setVegetationArea] = useState<number | undefined>(0);
    const [state, setState] = useState<string | undefined>("");
    const [name, setName] = useState<string | undefined>("");
    const [arableArea, setArableArea] = useState<number | undefined>(0);
    const [totalArea, setTotalArea] = useState<number | undefined>(0);
    const [city, setCity] = useState<string | undefined>("");

    const { modalIsOpen, setModalIsOpen, isEdit } = useContext(FarmModalContext);

    const { selectedOption, setRefreshCharts } = useContext(OptionsContext);
    const { farms, setFarms, selectedFarmId } = useContext(TablesContext);

    const [savedSuccessFullyMessage, setSavedSuccessFullyMessage] = useState(false);
    const [savedWithErrorMessage, setSavedWithErrorMessage] = useState(false);

    const selectedFarm = farms.find(farm => farm.id === selectedFarmId);

    useEffect(() => {
        if (isEdit && selectedFarm) {
            setVegetationArea(selectedFarm?.vegetation_area);
            setState(selectedFarm?.state);
            setName(selectedFarm?.name);
            setArableArea(selectedFarm?.arable_area);
            setTotalArea(selectedFarm?.total_area);
            setCity(selectedFarm?.city);
        } else {
            setVegetationArea(0);
            setState("");
            setName("");
            setArableArea(0);
            setTotalArea(0);
            setCity("");
        }
    }, [isEdit, selectedFarm]);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        const newFarm = { vegetation_area: vegetationArea, state, name, arable_area: arableArea, total_area: totalArea, city, id: selectedOption?.id };
        if (isEdit) {
            const response = await API.put(`/api/v1/farm/${selectedFarm?.id}`, newFarm);

            if (response.status === 200) {
                setSavedSuccessFullyMessage(true);
                setTimeout(() => {
                    setSavedSuccessFullyMessage(false);
                }, 2000);
                setFarms((prevFarms) => prevFarms.map(farm => farm.id === selectedFarm?.id ? response.data as IFarm : farm));
                setRefreshCharts(previous => previous + 1);
            } else {
                setSavedWithErrorMessage(true);
                setTimeout(() => {
                    setSavedWithErrorMessage(false);
                }, 2000);
            }
        } else {
            const response = await API.post(`/api/v1/farmer/${selectedOption}/farm`, newFarm);

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
                setFarms((prevFarms) => [...prevFarms, response.data as IFarm]);
                setRefreshCharts(previous => previous + 1);
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