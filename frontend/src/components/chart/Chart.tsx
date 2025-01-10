import React, { useContext } from "react";
import { OptionsContext } from "../../context/OptionsContext";

export default function Chart() {
    const { selectedOption } = useContext(OptionsContext);

    return (
        <div>
            <h1>{selectedOption}</h1>
        </div>
    )
}