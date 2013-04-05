package ru.arkuzmin.refactor.exception;

public class IllegalInputException extends Exception {
	
	private static final long serialVersionUID = 2250102781944399920L;

	public IllegalInputException(String msg) {
		super(msg);
	}
}
