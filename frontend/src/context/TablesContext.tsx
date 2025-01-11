import React, { createContext, useState } from 'react';
import { ICrop, IFarm } from '../components/IFarmer';

export const TablesContext = createContext<{ 
    farms: IFarm[],
    setFarms: React.Dispatch<React.SetStateAction<IFarm[]>>
    crops: ICrop[],
    setCrops: React.Dispatch<React.SetStateAction<ICrop[]>>
  }>({
    farms: [],
    setFarms: () => null,
    crops: [],
    setCrops: () => null,
});

interface TablesContextProps {
  children: React.ReactNode;
}

export const TablesContextProvider = ({ children }: TablesContextProps) => {
  const [farms, setFarms] = useState<IFarm[]>([]);
  const [crops, setCrops] = useState<ICrop[]>([]);

  return (
    <TablesContext.Provider value={{ farms, setFarms, crops, setCrops }}>
      {children}
    </TablesContext.Provider>
  );
};
