import React from "react"
import { PaginatedSelect } from "../../components/paginated_select/PaginatedSelect";
import { OptionsProvider } from "../../context/OptionsContext";

export default function Dashboard() {
    const handleClick = () => {
        // Define the action to be triggered on button click
        console.log("Create button clicked");
    };

    return (
        <div>
            <div style={{ display: 'flex', flexDirection: 'row', alignItems: 'center' }}>
                <OptionsProvider>
                    <PaginatedSelect />
                </OptionsProvider>
                <button onClick={handleClick}>
                        Create
                </button>
            </div>
            <OptionsProvider>
                <p>body</p>
            </OptionsProvider>
        </div>

    )
}