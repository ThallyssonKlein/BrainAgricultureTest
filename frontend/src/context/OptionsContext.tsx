import React, { createContext, useState } from 'react';

export const OptionsContext = createContext<{
  options: any[];
  setOptions: React.Dispatch<React.SetStateAction<any[]>>;
  selectedOption: any;
  setSelectedOption: React.Dispatch<React.SetStateAction<any>>;
}>({
  options: [],
  setOptions: () => {},
  selectedOption: null,
  setSelectedOption: () => {}
});

interface OptionsproviderProps {
  children: React.ReactNode;
}

export const OptionsProvider = ({ children }: OptionsproviderProps) => {
  const [options, setOptions] = useState<any[]>([]);
  const [selectedOption, setSelectedOption] = useState(null);

  return (
    <OptionsContext.Provider value={{ options, setOptions, selectedOption, setSelectedOption }}>
      {children}
    </OptionsContext.Provider>
  );
};
