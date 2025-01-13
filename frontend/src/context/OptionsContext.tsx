import React, { createContext, useState } from 'react';
import IFarmer from '../components/IFarmer';

export const OptionsContext = createContext<{
  selectedOption: any;
  setSelectedOption: React.Dispatch<React.SetStateAction<any>>;
  refreshCharts: number;
  setRefreshCharts: React.Dispatch<React.SetStateAction<number>>;
  searchTerm: string;
  setSearchTerm: React.Dispatch<React.SetStateAction<string>>;
}>({
  selectedOption: null,
  setSelectedOption: () => {},
  refreshCharts: 0,
  setRefreshCharts: () => {},
  searchTerm: '',
  setSearchTerm: () => {},
});

interface OptionsproviderProps {
  children: React.ReactNode;
}

export const OptionsContextProvider = ({ children }: OptionsproviderProps) => {
  const [selectedOption, setSelectedOption] = useState<IFarmer | null>(null);
  const [refreshCharts, setRefreshCharts] = useState(0);
  const [searchTerm, setSearchTerm] = useState<string>('');

  return (
    <OptionsContext.Provider value={{ 
        selectedOption, 
        setSelectedOption,
        refreshCharts,
        setRefreshCharts,
        searchTerm,
        setSearchTerm,
      }}>
      {children}
    </OptionsContext.Provider>
  );
};
