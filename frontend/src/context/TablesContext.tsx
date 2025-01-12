import React, { createContext, useState } from 'react';
import { ICrop, IFarm } from '../components/IFarmer';

export const TablesContext = createContext<{ 
    farms: IFarm[],
    setFarms: React.Dispatch<React.SetStateAction<IFarm[]>>
    crops: ICrop[],
    setCrops: React.Dispatch<React.SetStateAction<ICrop[]>>
    selectedFarm: IFarm | null,
    setSelectedFarm: React.Dispatch<React.SetStateAction<IFarm | null>>
  }>({
    farms: [],
    setFarms: () => null,
    crops: [],
    setCrops: () => null,
    selectedFarm: null,
    setSelectedFarm: () => null,
});

interface TablesContextProps {
  children: React.ReactNode;
}

export const TablesContextProvider = ({ children }: TablesContextProps) => {
  const [farms, setFarms] = useState<IFarm[]>([]);
  const [crops, setCrops] = useState<ICrop[]>([]);
  const [selectedFarm, setSelectedFarm] = useState<IFarm | null>(null);

  return (
    <TablesContext.Provider value={{ 
                  farms, 
                  setFarms,
                  crops,
                  setCrops,
                  selectedFarm,
                  setSelectedFarm
        }}>
      {children}
    </TablesContext.Provider>
  );
};
