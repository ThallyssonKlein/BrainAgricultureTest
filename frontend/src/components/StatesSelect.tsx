import React from "react";

interface IStatesSelectProps {
    state: string;
    setState: (state: string) => void;
}

const brazilStates = [
    "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS", "MG",
    "PA", "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"
];

export default function StatesSelect({ state, setState }: IStatesSelectProps) {
    return (
        <select value={state} onChange={(e) => setState(e.target.value)} required>
            <option value="" disabled>Selecione um estado</option>
            {brazilStates.map((uf) => (
                <option key={uf} value={uf}>
                    {uf}
                </option>
            ))}
        </select>
    )
}