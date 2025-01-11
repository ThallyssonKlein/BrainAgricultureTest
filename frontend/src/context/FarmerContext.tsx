import React, { createContext, useState } from 'react';

export const FarmerContext = createContext<
    {
        name: string;
        setName: React.Dispatch<React.SetStateAction<string>>;
        state: string;
        setState: React.Dispatch<React.SetStateAction<string>>;
        city: string;
        setCity: React.Dispatch<React.SetStateAction<string>>;
        document: string;
        setDocument: React.Dispatch<React.SetStateAction<string>>;
        isEdit: boolean;
        setISEdit: React.Dispatch<React.SetStateAction<boolean>>;
        createFarmerMmodalIsOpen: boolean;
        setCreateFarmerMmodalIsOpen: React.Dispatch<React.SetStateAction<boolean>>;
    }
>({
    name: "",
    setName: () => {},
    state: "",
    setState: () => {},
    city: "",
    setCity: () => {},
    document: "",
    setDocument: () => {},
    isEdit: false,
    setISEdit: () => {},
    createFarmerMmodalIsOpen: false,
    setCreateFarmerMmodalIsOpen: () => {}
});

interface FarmerProviderProps {
  children: React.ReactNode;
}

export const FarmerContextProvider = ({ children }: FarmerProviderProps) => {
    const [name, setName] = useState("");
    const [state, setState] = useState("");
    const [city, setCity] = useState("");
    const [document, setDocument] = useState("");
    const [isEdit, setISEdit] = useState(false);
    const [createFarmerMmodalIsOpen, setCreateFarmerMmodalIsOpen] = useState(false);
  
    return (
        <FarmerContext.Provider value={{
            name,
            setName,
            state,
            setState,
            city,
            setCity,
            document,
            setDocument,
            isEdit,
            setISEdit,
            createFarmerMmodalIsOpen,
            setCreateFarmerMmodalIsOpen
        }}>
            {children}
        </FarmerContext.Provider>
    );
};
