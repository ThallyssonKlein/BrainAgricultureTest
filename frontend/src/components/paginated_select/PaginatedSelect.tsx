import React, { useState, useEffect, useRef, useContext, useCallback } from 'react';
import './PaginatedSelect.css';
import IFarmer from '../IFarmer';
import API from '../../API';
import { OptionsContext } from '../../context/OptionsContext';
import { TablesContext } from '../../context/TablesContext';

export const PaginatedSelect: React.FC = () => {
  const { selectedOption, setSelectedOption } = useContext(OptionsContext);
  const { setFarms, setCrops } = useContext(TablesContext);
  const [options, setOptions] = useState<IFarmer[]>([]);
  const [page, setPage] = useState<number>(1);
  const [hasMore, setHasMore] = useState<boolean>(true);
  const [searchTerm, setSearchTerm] = useState<string>('');
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [isOpen, setIsOpen] = useState<boolean>(false);
  const dropdownRef = useRef<HTMLDivElement | null>(null);

  const loadOptions = useCallback(
    async (page: number, searchTerm: string) => {
      const fetchOptions = async (page: number, searchTerm: string): Promise<IFarmer[]> => {
        const response = await API.get(`/api/v1/farmer?page=${page}&limit=10&query=${searchTerm}`);

        if (response.status !== 200) {
          alert('Error fetching farmers!');
          return [];
        }

        return response.data as IFarmer[];
      };

      setIsLoading(true);
      const newOptions: IFarmer[] = await fetchOptions(page, searchTerm);

      if (page === 1) {
        setOptions(newOptions);
        if (newOptions.length > 0) {
          const firstOption = newOptions[0];
          setSelectedOption(firstOption);
          setSearchTerm(firstOption.name);
          setFarms([]);
          setCrops([]);
        }
      } else {
        setOptions((prevOptions) => [...prevOptions, ...newOptions]);
      }

      setHasMore(newOptions.length > 0);
      setIsLoading(false);
    },
    [setOptions, setSelectedOption, setFarms, setCrops]
  );

  useEffect(() => {
    if (searchTerm !== '' || page === 1) {
      setPage(1);
      loadOptions(1, searchTerm);
    }
  }, [searchTerm, loadOptions, page]);

  useEffect(() => {
    if (isOpen && page > 1) {
      loadOptions(page, searchTerm);
    }
  }, [page, isOpen, loadOptions, searchTerm]);

  const handleScroll = () => {
    if (!dropdownRef.current) return;

    const { scrollTop, scrollHeight, clientHeight } = dropdownRef.current;
    if (scrollTop + clientHeight >= scrollHeight - 10 && hasMore && !isLoading) {
      setPage((prevPage) => prevPage + 1);
    }
  };

  const handleSearch = (event: React.ChangeEvent<HTMLInputElement>) => {
    const value = event.target.value;
    setSearchTerm(value);
  };

  const handleDropdownClick = () => {
    setIsOpen((prevIsOpen) => !prevIsOpen);
    if (!isOpen) {
      setPage(1);
      setHasMore(true);
    }
  };

  const handleOptionClick = (name: string, farmer: IFarmer) => {
    setSelectedOption(farmer);
    setFarms([]);
    setCrops([]);
    setSearchTerm(name);
    setTimeout(() => setIsOpen(false), 100);
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
          {options.length > 0 ? (
            options.map((option: IFarmer) => (
              <div
                key={option.id}
                className={`option-item ${selectedOption?.id === option.id ? 'selected' : ''}`}
                onClick={() => handleOptionClick(option.name, option)}
              >
                {option.name}
              </div>
            ))
          ) : (
            !isLoading && <div className="no-results">No results found</div>
          )}
          {isLoading && <div className="loading">Loading...</div>}
        </div>
      )}
    </div>
  );
};
