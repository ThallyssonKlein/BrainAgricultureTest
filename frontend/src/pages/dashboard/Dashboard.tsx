import React from "react"
import { PaginatedSelect } from "../../components/paginated_select/PaginatedSelect";
import { OptionsProvider } from "../../context/OptionsContext";
import Charts from "../../components/charts/Charts";

export default function Dashboard() {
    const handleClick = () => {
        // Define the action to be triggered on button click
        console.log("Create button clicked");
    };

    return (
        <OptionsProvider>
            <div>
                <div style={{ display: 'flex', flexDirection: 'row', alignItems: 'center' }}>
                        <PaginatedSelect />
                    <button onClick={handleClick}>
                            Create
                    </button>
                </div>
                <Charts />
            </div>
        </OptionsProvider>
    )
}