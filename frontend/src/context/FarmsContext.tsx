import React, { createContext, useState } from 'react';
import { IFarm } from '../components/paginated_select/IFarmer';

export const FarmsContext = createContext<{ farms: IFarm[], setFarms: React.Dispatch<React.SetStateAction<IFarm[]>> }>({
    farms: [],
    setFarms: () => null,
});

interface FarmsproviderProps {
  children: React.ReactNode;
}

export const FarmsProvider = ({ children }: FarmsproviderProps) => {
  const [farms, setFarms] = useState<IFarm[]>([]);

  return (
    <FarmsContext.Provider value={{ farms, setFarms }}>
      {children}
    </FarmsContext.Provider>
  );
};
