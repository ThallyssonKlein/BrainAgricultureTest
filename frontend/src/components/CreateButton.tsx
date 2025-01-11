import React, { useContext } from "react";
import { FarmerContext } from "../context/FarmerContext";

export default function CreateButton() {
    const { setISEdit, setCreateFarmerMmodalIsOpen } = useContext(FarmerContext);

    return (
        <button
            onClick={() => {
                setISEdit(false);
                setCreateFarmerMmodalIsOpen(true);
            }}
        >Create</button>
    );
}