import React, { useContext } from "react";
import { FarmerModalContext } from "../context/FarmerModalContext";

export default function EditFarmerButton() {
    const { setISEdit, setModalIsOpen } = useContext(FarmerModalContext);

    return (
        <button
            onClick={() => {
                setISEdit(true);
                setModalIsOpen(true);
            }}
        >Edit</button>
    );
}