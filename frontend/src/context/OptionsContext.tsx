import React, { createContext, useState } from 'react';
import IFarmer from '../components/IFarmer';

export const OptionsContext = createContext<{
  selectedOption: any;
  setSelectedOption: React.Dispatch<React.SetStateAction<any>>;
  refreshCharts: number;
  setRefreshCharts: React.Dispatch<React.SetStateAction<number>>;
}>({
  selectedOption: null,
  setSelectedOption: () => {},
  refreshCharts: 0,
  setRefreshCharts: () => {},
});

interface OptionsproviderProps {
  children: React.ReactNode;
}

export const OptionsContextProvider = ({ children }: OptionsproviderProps) => {
  const [selectedOption, setSelectedOption] = useState<IFarmer | null>(null);
  const [refreshCharts, setRefreshCharts] = useState(0);

  return (
    <OptionsContext.Provider value={{ 
        selectedOption, 
        setSelectedOption,
        refreshCharts,
        setRefreshCharts,
      }}>
      {children}
    </OptionsContext.Provider>
  );
};
