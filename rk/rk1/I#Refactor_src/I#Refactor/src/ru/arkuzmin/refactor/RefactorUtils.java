package ru.arkuzmin.refactor;

import java.util.LinkedList;
import java.util.List;

import ru.arkuzmin.refactor.exception.IllegalInputException;

public class RefactorUtils {
	
	public static List<String> refactor(String input) throws Exception {
		List<String> refactoredList = new LinkedList<String>();
		String commonType = null;
		// Удаляем символ окончания строки
		if (input.endsWith(Globals.StringConstants.ENDLN)) {
			input = input.substring(0, input.length() - 1);
		} else {
			throw new IllegalInputException("RefactorUtils_EXCEPTION: Некорректные входные данные, строка должна заканчиваться на \";\"");
		}
		
		// Переменные 
		String[] vars = getVars(input);
		
		// Общий тип
		if (vars != null && vars.length > 0) {
			commonType = getCommonType(vars[0]);
		} else {
			throw new IllegalInputException("RefactorUtils_EXCEPTION: Некорректные входные данные, строка не содержит переменных");
		}
		
		vars[0] = vars[0].replaceAll(escString(commonType), Globals.StringConstants.EMPTY_STRING);
		
		for (int i = 0; i < vars.length; i++) {
			String inputVT = vars[i];
			String[] varAndType = getVarAndSpecType(inputVT);
			String line = commonType + revertType(varAndType[1]) + Globals.StringConstants.SPACE + varAndType[0] + Globals.StringConstants.ENDLN;
			refactoredList.add(line);
		}
		
		return refactoredList;
	}
	
	
	private static String[] getVarAndSpecType(String varAndType) throws Exception { 
		varAndType = varAndType.trim();
		StringBuilder var = new StringBuilder(Globals.StringConstants.EMPTY_STRING);
		StringBuilder specType = new StringBuilder(Globals.StringConstants.EMPTY_STRING);
		String[] result = new String[2];
		
		int i = 0;
		
		// Переменная
		while (i < varAndType.length()) {
			char ch = varAndType.charAt(i);
			if (Character.isLetter(ch)) {
				var.append(ch);
				i++;
			} else {
				break;
			}
		}
		
		// Тип переменной
		while (i < varAndType.length()) {
			char ch = varAndType.charAt(i);
			if (Globals.operations.contains(ch)) {
				specType.append(ch);
				i++;
			} else {
				break;
			}
		}
		
		if ((var.length() + specType.length()) != varAndType.length()) {
			throw new IllegalInputException("RefactorUtils_EXCEPTION: Некорректные входные данные: " + varAndType);
		}
		
		result[0] = var.toString();
		result[1] = specType.toString();
		
		return result;
	}
	
	private static String[] getVars(String input) {
		return input.split(Globals.SplitConstants.VARS_SEPARATOR);
	}
	
	private static String escString(String input) {
		StringBuilder esc = new StringBuilder(Globals.StringConstants.EMPTY_STRING);
		
		int i = 0;
		while (i < input.length()) {
			char ch = input.charAt(i);
			if (Globals.operations.contains(ch)) {
				esc.append("\\").append(ch);
			} else {
				esc.append(ch);
			}
			i++;
		}
		
		return esc.toString();
	}
	
	private static String getCommonType(String firstVar) throws Exception {
		String[] typeVar = firstVar.split(Globals.StringConstants.SPACE);
		String commonType = null;
		
		if (typeVar != null && typeVar.length == 2) {
			commonType = typeVar[0];
		} else {
			throw new IllegalInputException("RefactorUtils_EXCEPTION: Не удалось получить тип, общий для всех переменных ");
		}
		
		return commonType;
	}
	
	private static String revertType(String type) throws Exception {
		
		if (type == null || type.equals(Globals.StringConstants.EMPTY_STRING)) {
			return type;
		}
		
		String reversed = new StringBuilder(type).reverse().toString();
		reversed = reversed.replaceAll("\\[", "_");
		reversed = reversed.replaceAll("\\]", "[");
		reversed = reversed.replaceAll("_", "]");
		
		return reversed;
	}
	
}
