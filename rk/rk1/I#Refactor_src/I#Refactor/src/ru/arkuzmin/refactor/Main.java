package ru.arkuzmin.refactor;

import java.util.List;

public class Main {
	
	public static void main(String[] args) {
		//String input = "int& a*[]&, b, c*;";
		String input = "Double[][] Array[];";
		//String input = ";";
		List<String> output = null;
		try {
			output = RefactorUtils.refactor(input);
			System.out.println(output);
		} catch (Exception e) {
			System.out.println(e);
		}
	}
}
