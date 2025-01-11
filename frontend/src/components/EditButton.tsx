import React, { useContext } from "react";
import { FarmerContext } from "../context/FarmerContext";

export default function EditButton() {
    const { setISEdit, setCreateFarmerMmodalIsOpen } = useContext(FarmerContext);

    return (
        <button
            onClick={() => {
                setISEdit(true);
                setCreateFarmerMmodalIsOpen(true);
            }}
        >Edit</button>
    );
}