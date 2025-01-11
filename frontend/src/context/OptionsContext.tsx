import React, { createContext, useState } from 'react';

export const OptionsContext = createContext<{
  options: any[];
  setOptions: React.Dispatch<React.SetStateAction<any[]>>;
  selectedOption: any;
  setSelectedOption: React.Dispatch<React.SetStateAction<any>>;
  selectedObject: any;
  setSelectedObject: React.Dispatch<React.SetStateAction<any>>;
  refreshKey: number;
  setRefreshKey: React.Dispatch<React.SetStateAction<number>>;
}>({
  options: [],
  setOptions: () => {},
  selectedOption: null,
  setSelectedOption: () => {},
  selectedObject: null,
  setSelectedObject: () => {},
  refreshKey: 0,
  setRefreshKey: () => {},
});

interface OptionsproviderProps {
  children: React.ReactNode;
}

export const OptionsContextProvider = ({ children }: OptionsproviderProps) => {
  const [options, setOptions] = useState<any[]>([]);
  const [selectedOption, setSelectedOption] = useState(null);
  const [selectedObject, setSelectedObject] = useState(null);
  const [refreshKey, setRefreshKey] = useState(0);

  return (
    <OptionsContext.Provider value={{ 
        options, 
        setOptions, 
        selectedOption, 
        setSelectedOption,
        selectedObject,
        setSelectedObject,
        refreshKey,
        setRefreshKey,
      }}>
      {children}
    </OptionsContext.Provider>
  );
};
