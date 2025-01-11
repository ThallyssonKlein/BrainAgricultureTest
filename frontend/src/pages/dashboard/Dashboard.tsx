import React, { useState } from "react"
import { PaginatedSelect } from "../../components/paginated_select/PaginatedSelect";
import { OptionsContextProvider } from "../../context/OptionsContext";
import Charts from "../../components/charts/Charts";
import { TablesContextProvider } from "../../context/TablesContext";
import Tables from "../../components/table/Tables";
import CreateFarmerModal from "../../components/CreateFarmerModal";
import { FarmerModalContextProvider } from "../../context/FarmerModalContext";
import CreateFarmerButton from "../../components/CreateFarmerButton";
import EditFarmerButton from "../../components/EditFarmerButton";
import DeleteFarmerButton from "../../components/DeleteFarmerButton";
import { FarmModalContextProvider } from "../../context/FarmModalContext";
import CreateFarmButton from "../../components/CreateFarmButton";
import CreateFarmModal from "../../components/CreateFarmModal";

export default function Dashboard() {
        return (
        <OptionsContextProvider>
            <FarmerModalContextProvider>
                <FarmModalContextProvider>
                    <CreateFarmerModal />
                    <CreateFarmModal />
                    <div>
                        <div style={{ display: 'flex', flexDirection: 'row', alignItems: 'center' }}>
                                <PaginatedSelect />
                                <CreateFarmerButton />
                                <EditFarmerButton />
                                <DeleteFarmerButton />
                        </div>
                        <div style={{ display: 'flex', flexDirection: 'row', alignItems: 'center' }}>
                                <CreateFarmButton />
                        </div>
                        <TablesContextProvider>
                            <Charts />
                            <Tables />
                        </TablesContextProvider>
                    </div>
                </FarmModalContextProvider>
            </FarmerModalContextProvider>
        </OptionsContextProvider>
    )
}