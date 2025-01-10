/* eslint-disable testing-library/no-unnecessary-act */
import React, { act } from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { PaginatedSelect } from './PaginatedSelect';
import API from '../../API';

jest.mock('../../API', () => ({
  get: jest.fn(),
}));

const mockSetSelectedOption = jest.fn();
const mockSetOptions = jest.fn();

const mockOptions = [
  { id: 1, nickname: 'Player1', gold: 100 },
  { id: 2, nickname: 'Player2', gold: 200 },
  { id: 3, nickname: 'Player3', gold: 300 },
];

describe('PaginatedSelect Component', () => {
  beforeAll(() => {
    jest.spyOn(window, 'alert').mockImplementation(() => {});
  });

  afterAll(() => {
    jest.restoreAllMocks();
  });

  beforeEach(() => {
    (API.get as jest.Mock).mockImplementation((url: string) => {
      if (url.includes('search')) {
        return Promise.resolve({
          status: 200,
          data: mockOptions,
        });
      }
      return Promise.resolve({
        status: 200,
        data: [],
      });
    });

    jest.clearAllMocks();
  });

  test('displays loading indicator while fetching', async () => {
    (API.get as jest.Mock).mockImplementationOnce(
      () =>
        new Promise((resolve) =>
          setTimeout(
            () =>
              resolve({
                status: 200,
                data: mockOptions,
              }),
            500
          )
        )
    );

    render(
      <PaginatedSelect
        selectedOption={null}
        setSelectedOption={mockSetSelectedOption}
        options={[]}
        setOptions={mockSetOptions}
      />
    );

    const input = screen.getByPlaceholderText('Search...');
    await act(async () => {
      fireEvent.click(input);
    });

    await waitFor(() => {
      expect(screen.getByText('Loading...')).toBeInTheDocument();
    });

    await waitFor(() => {
      expect(screen.queryByText('Loading...')).not.toBeInTheDocument();
    });
  });

  test('renders input and dropdown', () => {
    render(
      <PaginatedSelect
        selectedOption={null}
        setSelectedOption={mockSetSelectedOption}
        options={[]}
        setOptions={mockSetOptions}
      />
    );

    expect(screen.getByPlaceholderText('Search...')).toBeInTheDocument();
  });

  test('opens dropdown on input click', async () => {
    render(
      <PaginatedSelect
        selectedOption={null}
        setSelectedOption={mockSetSelectedOption}
        options={[]}
        setOptions={mockSetOptions}
      />
    );

    const input = screen.getByPlaceholderText('Search...');
    await act(async () => {
      fireEvent.click(input);
    });

    await waitFor(() => {
      expect(screen.getByRole('listbox')).toBeInTheDocument();
    });
  });

  test('calls fetchOptions on open and loads options', async () => {
    render(
      <PaginatedSelect
        selectedOption={null}
        setSelectedOption={mockSetSelectedOption}
        options={[]}
        setOptions={mockSetOptions}
      />
    );

    const input = screen.getByPlaceholderText('Search...');
    await act(async () => {
      fireEvent.click(input);
    });

    await waitFor(() => {
      expect(API.get).toHaveBeenCalledWith(
        '/api/v1/player/search?page=1&limit=10&search='
      );
    });

    await waitFor(() => {
      expect(mockSetOptions).toHaveBeenCalledWith(mockOptions);
    });
  });

  test('filters options on search input change', async () => {
    render(
      <PaginatedSelect
        selectedOption={null}
        setSelectedOption={mockSetSelectedOption}
        options={[]}
        setOptions={mockSetOptions}
      />
    );

    const input = screen.getByPlaceholderText('Search...');
    await act(async () => {
      userEvent.type(input, 'Player1');
    });

    await waitFor(() => {
      expect(API.get).toHaveBeenCalledWith(
        '/api/v1/player/search?page=1&limit=10&search=Player1'
      );
    });
  });

  test('selects an option and updates state', async () => {
    render(
      <PaginatedSelect
        selectedOption={null}
        setSelectedOption={mockSetSelectedOption}
        options={mockOptions}
        setOptions={mockSetOptions}
      />
    );

    const input = screen.getByPlaceholderText('Search...');
    await act(async () => {
      fireEvent.click(input);
    });

    const option = screen.getByText('Player1');
    await act(async () => {
      fireEvent.click(option);
    });

    await waitFor(() => {
      expect(mockSetSelectedOption).toHaveBeenCalledWith('Player1');
      expect(input).toHaveValue('Player1');
    });
  });

  test('loads more options on scroll to bottom', async () => {
    render(
      <PaginatedSelect
        selectedOption={null}
        setSelectedOption={mockSetSelectedOption}
        options={mockOptions}
        setOptions={mockSetOptions}
      />
    );

    const input = screen.getByPlaceholderText('Search...');
    await act(async () => {
      fireEvent.click(input);
    });

    const dropdown = screen.getByRole('listbox');
    await act(async () => {
      fireEvent.scroll(dropdown, { target: { scrollTop: 100 } });
    });

    await waitFor(() => {
      expect(API.get).toHaveBeenCalledWith(
        '/api/v1/player/search?page=2&limit=10&search='
      );
    });
  });

  test('handles empty results gracefully', async () => {
    (API.get as jest.Mock).mockResolvedValueOnce({
      status: 200,
      data: [],
    });

    render(
      <PaginatedSelect
        selectedOption={null}
        setSelectedOption={mockSetSelectedOption}
        options={[]}
        setOptions={mockSetOptions}
      />
    );

    const input = screen.getByPlaceholderText('Search...');
    await act(async () => {
      fireEvent.click(input);
    });

    await waitFor(() => {
      expect(screen.getByText('No more options')).toBeInTheDocument();
    });
  });

  test('handles API errors gracefully', async () => {
    (API.get as jest.Mock).mockResolvedValueOnce({
      status: 500,
      data: [],
    });

    render(
      <PaginatedSelect
        selectedOption={null}
        setSelectedOption={mockSetSelectedOption}
        options={[]}
        setOptions={mockSetOptions}
      />
    );

    const input = screen.getByPlaceholderText('Search...');
    await act(async () => {
      fireEvent.click(input);
    });

    await waitFor(() => {
      expect(API.get).toHaveBeenCalled();
    });
  });
});
