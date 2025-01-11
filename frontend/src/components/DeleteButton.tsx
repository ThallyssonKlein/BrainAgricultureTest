import React, { useContext } from "react";
import { OptionsContext } from "../context/OptionsContext";
import API from "../API";

export default function DeleteButton() {
    const { selectedOption } = useContext(OptionsContext);

    const handleOnClick = async () => {
        const response = await API.delete(`/api/v1/farmer/${selectedOption.id}`);

        if (response.status !== 200) {
            alert('Error deleting farmer!');
        } else {
            window.location.reload();
        }
    }

    return (
        <button
            onClick={handleOnClick}
        >Delete</button>
    );
}