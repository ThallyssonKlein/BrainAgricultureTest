import React, { useState, useContext, useEffect } from "react";
import Modal from "react-modal";
import { FarmModalContext } from "../context/FarmModalContext";
import { OptionsContext } from "../context/OptionsContext";
import API from "../API";
import { TablesContext } from "../context/TablesContext";
import { IFarm } from "./IFarmer";
import StatesSelect from "./StatesSelect";
import messageTranslations from '../messageTranslations';

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

        if (vegetationArea && vegetationArea <= 0) {
            alert("A área de vegetação deve ser maior que 0!");
            return;
        }

        if (arableArea && arableArea <= 0) {
            alert("A área de cultivo deve ser maior que 0!");
            return;
        }

        if ((name || "").length > 255) {
            alert("O nome deve ter no máximo 255 caracteres!");
            return;
        }

        if ((city || "").length > 255) {
            alert("A cidade deve ter no máximo 255 caracteres!");
            return;
        }

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
        } else {
            const response = await API.post(`/api/v1/farmer/${selectedOption.id}/farm`, newFarm);

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
        setTotalArea((vegetationArea || 0) + (arableArea || 0));
    }, [arableArea, vegetationArea]);

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
            <h2>{isEdit ? "Edite a Fazenda" : "Crie uma Fazenda"}</h2>
            <form
                style={{
                    display: 'grid',          
                    gridTemplateColumns: '1fr 1fr', 
                    gap: '20px',              
                    position: 'relative',     
                    paddingBottom: '60px',    
                }}
                onSubmit={handleSubmit}>
                <label style={{ marginRight: 20}}>Área de Vegetação</label>
                <input type="number" value={vegetationArea} onChange={(e) => setVegetationArea(Number(e.target.value))} required />

                <label style={{ marginRight: 20}}>Estado</label>
                <StatesSelect state={state || ""} setState={setState} />

                <label style={{ marginRight: 20}}>Nome</label>
                <input type="text" value={name} onChange={(e) => setName(e.target.value)} required />

                <label style={{ marginRight: 20}}>Área de Cultivo</label>
                <input type="number" value={arableArea} onChange={(e) => setArableArea(Number(e.target.value))} required />

                <label style={{ marginRight: 20}}>Área Total</label>
                <label>{totalArea}</label>

                <label style={{ marginRight: 20}}>Cidade</label>
                <input type="text" value={city} onChange={(e) => setCity(e.target.value)} required />

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
                {savedSuccessFullyMessage && <p>Salvo com sucesso!</p>}
                {savedWithErrorMessage && <p>Algo deu errado!</p>}
            </form>
    </Modal>
    )
}