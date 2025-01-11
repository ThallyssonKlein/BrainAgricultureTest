import React, { useContext } from "react";
import { FarmerModalContext } from "../context/FarmerModalContext";

export default function CreateFarmerButton() {
    const { setISEdit, setModalIsOpen } = useContext(FarmerModalContext);

    return (
        <button
            onClick={() => {
                setISEdit(false);
                setModalIsOpen(true);
            }}
        >Create</button>
    );
}