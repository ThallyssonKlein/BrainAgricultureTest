import React, { useContext } from "react";
import { FarmerModalContext } from "../context/FarmerModalContext";

export default function EditFarmerButton() {
    const { setISEdit, setModalIsOpen } = useContext(FarmerModalContext);

    return (
        <button
            style={{ marginRight: 10 }}
            onClick={() => {
                setISEdit(true);
                setModalIsOpen(true);
            }}
        >Editar</button>
    );
}