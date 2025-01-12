import React, { useState, useEffect, useContext } from "react";
import Modal from "react-modal";
import API from "../API";
import { FarmerModalContext } from "../context/FarmerModalContext";
import { OptionsContext } from "../context/OptionsContext";
import StatesSelect from "./StatesSelect";

export default function FarmerModal() {
    const [name, setName] = useState("");
    const [state, setState] = useState("");
    const [city, setCity] = useState("");
    const [document, setDocument] = useState("");

    const [savedSuccessFullyMessage, setSavedSuccessFullyMessage] = useState(false);
    const [savedWithErrorMessage, setSavedWithErrorMessage] = useState(false);

    const {
        isEdit,
        modalIsOpen,
        setModalIsOpen
    } = useContext(FarmerModalContext);

    const { selectedOption } = useContext(OptionsContext);

    useEffect(() => {
        if (isEdit && selectedOption) {
            setName(selectedOption.name);
            setState(selectedOption.state);
            setCity(selectedOption.city);
            setDocument(selectedOption.document);
        } else {
            setName("");
            setState("");
            setCity("");
            setDocument("");
        }
    }, [isEdit, selectedOption]);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        const newFarmer = { name, state, city, document, id: selectedOption?.id };
        if (isEdit) {
            const response = await API.put(`/api/v1/farmer/${selectedOption?.id}`, newFarmer);

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
            const response = await API.post("/api/v1/farmer", newFarmer);

            if (response.status === 201) {
                setSavedSuccessFullyMessage(true);
                setTimeout(() => {
                    setSavedSuccessFullyMessage(false);
                }, 2000);
                setName("");
                setState("");
                setCity("");
                setDocument("");
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
            <h2>{isEdit ? "Editar Fazendeiro" : "Cadastrar Fazendeiro"}</h2>
            <form 
                style={{
                    display: 'grid',
                    gridTemplateColumns: '1fr 1fr',
                    gap: '20px',
                    position: 'relative',
                    paddingBottom: '60px',
                }}
                onSubmit={handleSubmit}>
                <label>Nome</label>
                <input type="text" value={name} onChange={(e) => setName(e.target.value)} required />
               
                <label>Estado</label>
                <StatesSelect state={state} setState={setState} />
                <label>Cidade</label>
                <input type="text" value={city} onChange={(e) => setCity(e.target.value)} required />

                <label>Documento (CPF ou CNPJ)</label>
                <input type="text" value={document} onChange={(e) => setDocument(e.target.value)} required />

                <button
                    style={{
                        position: 'absolute',
                        bottom: '10px',
                        right: '20px',
                        marginLeft: '30px',
                        cursor: 'pointer',
                    }}                     
                    type="submit">{isEdit ? "Atualizar" : "Salvar"}</button>
                {savedSuccessFullyMessage && <p>Salvo com sucesso!</p>}
                {savedWithErrorMessage && <p>Algo deu errado!</p>}
            </form>
        </Modal>
    );
}
