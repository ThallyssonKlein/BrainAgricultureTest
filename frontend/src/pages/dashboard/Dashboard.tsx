import React, { useState } from "react"
import { PaginatedSelect } from "../../components/paginated_select/PaginatedSelect";
import { OptionsContextProvider } from "../../context/OptionsContext";
import Charts from "../../components/charts/Charts";
import { TablesContextProvider } from "../../context/TablesContext";
import Tables from "../../components/table/Tables";
import FarmerModal from "../../components/FarmerModal";
import { FarmerModalContextProvider } from "../../context/FarmerModalContext";
import CreateFarmerButton from "../../components/CreateFarmerButton";
import EditFarmerButton from "../../components/EditFarmerButton";
import DeleteFarmerButton from "../../components/DeleteFarmerButton";
import { FarmModalContextProvider } from "../../context/FarmModalContext";
import CreateFarmButton from "../../components/CreateFarmButton";
import FarmModal from "../../components/FarmModal";
import { CropModalContextProvider } from "../../context/CropModalContext";

export default function Dashboard() {
        return (
        <OptionsContextProvider>
            <FarmerModalContextProvider>
                <FarmModalContextProvider>
                    <TablesContextProvider>
                        <FarmerModal />
                        <FarmModal />
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
                                <Charts />
                                <CropModalContextProvider>
                                    <Tables />
                                </CropModalContextProvider>
                        </div>
                    </TablesContextProvider>
                </FarmModalContextProvider>
            </FarmerModalContextProvider>
        </OptionsContextProvider>
    )
}