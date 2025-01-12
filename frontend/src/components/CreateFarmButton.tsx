import React, { useContext } from "react";
import { FarmModalContext } from "../context/FarmModalContext";
import { OptionsContext } from "../context/OptionsContext";

export default function CreateFarmButton() {
    const { setISEdit, setModalIsOpen } = useContext(FarmModalContext);
    const { selectedOption } = useContext(OptionsContext)

    return (
        <button
            style={{ flex: 1 }}
            onClick={() => {
                if (!selectedOption) {
                    alert("Please select a farmer first");
                } else {
                    setISEdit(false);
                    setModalIsOpen(true);
                }
            }}
        >Criar Fazenda</button>
    );
}