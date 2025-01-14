import React from "react";
import { ICulture } from "./IFarmer";

interface ICulturesTableProps {
    cultures: ICulture[];
    setSelectedCulture: (cultureId: number | null | undefined) => void;
    selectedCulture: number | null | undefined;
    setIsEditCulture: (isEditCulture: boolean) => void;
    setCultureModalIsOpen: (cultureModalIsOpen: boolean) => void;
    handleDeleteCulture: (cultureId: number | undefined) => void;
}

export default function CulturesTable({ cultures, 
                                        setSelectedCulture,
                                        selectedCulture,
                                        setIsEditCulture,
                                        setCultureModalIsOpen,
                                        handleDeleteCulture }: ICulturesTableProps) {
    return (
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
                            style={{ cursor: 'pointer', background: selectedCulture === culture.id ? '#adacac' : 'white' }}
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
                                >Editar</button>
                            </td>
                            <td>
                                <button onClick={(_event) => handleDeleteCulture(culture.id)}>Excluir</button>
                            </td>
                        </tr>                  
                    ))
                }
                </tbody>
            </table>
            <div style={{ display: 'flex', flexDirection: 'row', alignItems: 'center' }}>
                <button 
                    style={{flex: 1, marginBottom: 50}}
                    onClick={() => {
                        setIsEditCulture(false);
                        setCultureModalIsOpen(true);
                    }}
                >Criar Cultura</button>
            </div>
        </div>
    )
}