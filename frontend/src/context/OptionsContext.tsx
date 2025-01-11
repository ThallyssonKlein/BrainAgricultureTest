import React, { createContext, useState } from 'react';

export const OptionsContext = createContext<{
  options: any[];
  setOptions: React.Dispatch<React.SetStateAction<any[]>>;
  selectedOption: any;
  setSelectedOption: React.Dispatch<React.SetStateAction<any>>;
  selectedObject: any;
  setSelectedObject: React.Dispatch<React.SetStateAction<any>>;
}>({
  options: [],
  setOptions: () => {},
  selectedOption: null,
  setSelectedOption: () => {},
  selectedObject: null,
  setSelectedObject: () => {},
});

interface OptionsproviderProps {
  children: React.ReactNode;
}

export const OptionsContextProvider = ({ children }: OptionsproviderProps) => {
  const [options, setOptions] = useState<any[]>([]);
  const [selectedOption, setSelectedOption] = useState(null);
  const [selectedObject, setSelectedObject] = useState(null);

  return (
    <OptionsContext.Provider value={{ 
        options, 
        setOptions, 
        selectedOption, 
        setSelectedOption,
        selectedObject,
        setSelectedObject
      }}>
      {children}
    </OptionsContext.Provider>
  );
};
