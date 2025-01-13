import React, { useState, useEffect, useRef, useContext, useCallback } from 'react';
import './PaginatedSelect.css';
import IFarmer from '../IFarmer';
import API from '../../API';
import { OptionsContext } from '../../context/OptionsContext';
import { TablesContext } from '../../context/TablesContext';

export const PaginatedSelect: React.FC = () => {
  const { selectedOption, setSelectedOption } = useContext(OptionsContext)
  const [options, setOptions] = useState<IFarmer[]>([]);
  const [page, setPage] = useState<number>(1);
  const [hasMore, setHasMore] = useState<boolean>(true);
  const [searchTerm, setSearchTerm] = useState<string>('');
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [isOpen, setIsOpen] = useState<boolean>(false);
  const dropdownRef = useRef<HTMLDivElement | null>(null);
  const { setFarms, setCrops } = useContext(TablesContext);
  
  const fetchOptions = async (page: number, searchTerm: string): Promise<IFarmer[]> => {
    const response = await API.get(`/api/v1/farmer?page=${page}&limit=10&query=${searchTerm}`);

    if (response.status !== 200) {
      alert('Error fetching farmers!');
    }

    return (response.data as IFarmer[]);
  };

  const loadOptions = useCallback(async (page: number, searchTerm: string) => {
    setIsLoading(true);
    const newOptions: IFarmer[] = await fetchOptions(page, searchTerm);
    if (newOptions.length === 0) {
      setHasMore(false);
    } else {
      setOptions((prevOptions) => [...prevOptions, ...newOptions]);
    }
    setIsLoading(false);
  }, [setOptions]);

  useEffect(() => {
    if (isOpen) {
      loadOptions(page, searchTerm);
    }
  }, [page, searchTerm, isOpen, loadOptions]);

  useEffect(() => {
    (async () => {
      const newOptions: IFarmer[] = await fetchOptions(1, "");
      setSelectedOption(newOptions[0]);
      setSearchTerm(newOptions[0].name);
    })()
  }, [setSelectedOption])

  const handleScroll = () => {
    if (!dropdownRef.current) return;

    const { scrollTop, scrollHeight, clientHeight } = dropdownRef.current;
    if (scrollTop + clientHeight >= scrollHeight - 10 && hasMore && !isLoading) {
      setPage((prevPage) => prevPage + 1);
    }
  };

  const handleSearch = (event: React.ChangeEvent<HTMLInputElement>) => {
    setSearchTerm(event.target.value);
    setOptions([]); 
    setPage(1);
    setHasMore(true);
  };

  const handleDropdownClick = () => {
    setIsOpen((prevIsOpen) => !prevIsOpen);
    if (!isOpen) {
      setOptions([]);
      setPage(1);
      setHasMore(true);
    }
  };

  const handleOptionClick = (name: string, farmer: IFarmer) => {
    setSelectedOption(farmer);
    setCrops([]);
    setFarms([]);
    setSearchTerm(name);
    setTimeout(() => setIsOpen(false), 100)
  };

  return (
    <div className="paginated-select">
      <input
        type="text"
        placeholder="Search..."
        value={searchTerm}
        onChange={handleSearch}
        className="search-input"
        onClick={handleDropdownClick}
      />
      {isOpen && (
        <div
          className="options-dropdown"
          ref={dropdownRef}
          onScroll={handleScroll}
          role="listbox"
        >
          {options.map((option: IFarmer, index) => (
            <div
              key={index}
              className={`option-item ${selectedOption === option.name ? 'selected' : ''}`}
              onClick={() => handleOptionClick(option.name, option)}
            >
              {option.name}
            </div>
          ))}
          {isLoading && <div className="loading">Loading...</div>}
          {!hasMore && <div className="no-more">No more options</div>}
        </div>
      )}
    </div>
  );
};