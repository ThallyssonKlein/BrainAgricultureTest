import React, { useContext } from "react";
import { FarmModalContext } from "../context/FarmModalContext";

export default function CreateFarmButton() {
    const { setISEdit, setModalIsOpen } = useContext(FarmModalContext);

    return (
        <button
            style={{ flex: 1 }}
            onClick={() => {
                console.log("setou pra true")
                setISEdit(false);
                setModalIsOpen(true);
            }}
        >Create Farm</button>
    );
}