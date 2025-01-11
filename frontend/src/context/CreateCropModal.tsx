import React, { useState, useContext, useEffect } from "react";
import Modal from "react-modal";
import { OptionsContext } from "../context/OptionsContext";
import API from "../API";
import { CropModalContext } from "./CropModalContext";
import CreateCultureModal from "../components/CreateCultureModal";
import { ICulture } from "../components/IFarmer";

export default function CreateCropModal() {
    const [date, setDate] = useState<string>("");
    const [cultureNames, setCultureNames] = useState<string[]>([]);
    const { modalIsOpen, setModalIsOpen, isEdit } = useContext(CropModalContext);
    const { selectedOption, refreshKey, setRefreshKey } = useContext(OptionsContext);
    const [savedSuccessFullyMessage, setSavedSuccessFullyMessage] = useState(false);
    const [savedWithErrorMessage, setSavedWithErrorMessage] = useState(false);
    const [isEditCulture, setIsEditCulture] = useState(false);
    const [cultureModalIsOpen, setCultureModalIsOpen] = useState(false);
    const [cultures, setCultures] = useState<ICulture[]>([]);
    const [selectedCulture, setSelectedCulture] = useState<number | null>(null);

    useEffect(() => {
        if (isEdit && selectedOption) {
            // setVegetationArea(selectedOption.vegetation_area);
            // setState(selectedOption.state);
            // setName(selectedOption.name);
            // setArableArea(selectedOption.arable_area);
            // setTotalArea(selectedOption.total_area);
            // setCity(selectedOption.city);
        } else {
            setDate("");
            setCultureNames([]);
        }
    }, [isEdit, selectedOption]);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        const newCrop = { date, culture: { id: selectedCulture } };
        if (isEdit) {
            const response = await API.put(`/api/v1/farmer/${selectedOption}/crop`, newCrop);

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
            const response = await API.post(`/api/v1/farmer/${selectedOption}/crop`, newCrop);
            if (response.status === 201) {
                setSavedSuccessFullyMessage(true);
                setTimeout(() => {
                    setSavedSuccessFullyMessage(false);
                }, 2000);
                setDate("");
                setSelectedCulture(null);
                setRefreshKey(refreshKey + 1);
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
            const response = await API.get("/api/v1/culture");
            
            if (response.status === 200) {
                setCultures(response.data as ICulture[]);
            }
        })()
    }, [])

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
            <CreateCultureModal isEdit={isEditCulture} modalIsOpen={cultureModalIsOpen} setModalIsOpen={setCultureModalIsOpen}/>
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
                        <table border={1} style={{ width: '100%' }}>
                            <thead>
                            <tr>
                                <th>Id</th>
                                <th>Nome da Cultura</th>
                            </tr>
                            </thead>
                            <tbody>
                            {
                                cultures.map(culture => (
                                    <tr
                                        key={culture.id}
                                        onClick={() => setSelectedCulture(culture.id)}
                                        style={{ cursor: 'pointer', background: selectedCulture === culture.id ? '#f0f0f0' : 'white' }}
                                    >
                                        <td>{culture.id}</td>
                                        <td>{culture.name}</td>
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