import React, { createContext, useState } from 'react';
import { ICrop, IFarm } from '../components/IFarmer';

export const TablesContext = createContext<{ 
    farms: IFarm[],
    setFarms: React.Dispatch<React.SetStateAction<IFarm[]>>
    crops: ICrop[],
    setCrops: React.Dispatch<React.SetStateAction<ICrop[]>>
    selectedFarmId: number | null,
    setSelectedFarmId: React.Dispatch<React.SetStateAction<number | null>>
  }>({
    farms: [],
    setFarms: () => null,
    crops: [],
    setCrops: () => null,
    selectedFarmId: null,
    setSelectedFarmId: () => null,
});

interface TablesContextProps {
  children: React.ReactNode;
}

export const TablesContextProvider = ({ children }: TablesContextProps) => {
  const [farms, setFarms] = useState<IFarm[]>([]);
  const [crops, setCrops] = useState<ICrop[]>([]);
  const [selectedFarmId, setSelectedFarmId] = useState<number | null>(null);

  return (
    <TablesContext.Provider value={{ 
                  farms, 
                  setFarms,
                  crops,
                  setCrops,
                  selectedFarmId,
                  setSelectedFarmId
        }}>
      {children}
    </TablesContext.Provider>
  );
};
