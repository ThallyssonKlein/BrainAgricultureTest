import React, { useContext } from "react";
import { OptionsContext } from "../../context/OptionsContext";
import PieChart from "./PieChart";

export default function Charts() {
    const { selectedOption } = useContext(OptionsContext);

    return (
        <div>
            <h1>{selectedOption ? <PieChart /> : "Loading..." }</h1>
        </div>
    )
}