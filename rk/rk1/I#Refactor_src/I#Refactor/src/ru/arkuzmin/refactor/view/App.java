package ru.arkuzmin.refactor.view;
import java.awt.BorderLayout;
import java.awt.EventQueue;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.List;

import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JTextField;
import javax.swing.JTextPane;
import javax.swing.UIManager;
import javax.swing.UIManager.LookAndFeelInfo;

import ru.arkuzmin.refactor.RefactorUtils;


public class App {

	private JFrame frmIsharpRefactoring;
	private JTextPane output;
	private JTextField input;

	/**
	 * Launch the application.
	 */
	public static void main(String[] args) {
		EventQueue.invokeLater(new Runnable() {
			public void run() {
				try {
					
					    for (LookAndFeelInfo info : UIManager.getInstalledLookAndFeels()) {
					        if ("Nimbus".equals(info.getName())) {
					            UIManager.setLookAndFeel(info.getClassName());
					            break;
					        }
					    }
					
					App window = new App();
					window.frmIsharpRefactoring.setVisible(true);
				} catch (Exception e) {
					e.printStackTrace();
				}
			}
		});
	}

	/**
	 * Create the application.
	 */
	public App() {
		initialize();
	}

	/**
	 * Initialize the contents of the frame.
	 */
	private void initialize() {
		frmIsharpRefactoring = new JFrame();
		frmIsharpRefactoring.setTitle("ISharp Refactoring (Кузьмин А.Ю. ИУ7-29)");
		frmIsharpRefactoring.setResizable(false);
		frmIsharpRefactoring.setBounds(100, 100, 429, 296);
		frmIsharpRefactoring.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		frmIsharpRefactoring.getContentPane().setLayout(null);
		
		input = new JTextField();
		input.setBounds(10, 36, 403, 39);
		frmIsharpRefactoring.getContentPane().add(input);
		input.setColumns(10);
		
		JLabel lblNewLabel = new JLabel("Введите входные данные");
		lblNewLabel.setBounds(10, 11, 403, 14);
		frmIsharpRefactoring.getContentPane().add(lblNewLabel);
		
		JPanel panel = new JPanel();
		panel.setBounds(10, 111, 403, 146);
		frmIsharpRefactoring.getContentPane().add(panel);
		panel.setLayout(new BorderLayout(0, 0));
		
		JScrollPane scrollPane = new JScrollPane();
		panel.add(scrollPane, BorderLayout.CENTER);
		
		output = new JTextPane();
		scrollPane.setViewportView(output);
		
		JButton btnNewButton = new JButton("Рефакторинг");
		btnNewButton.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent arg0) {
				String inputStr = input.getText();
				try {
					output.setText("");
					List<String> outputList = RefactorUtils.refactor(inputStr);
					for (String out : outputList) {
						output.setText(output.getText() + "\n" + out);
					}
				} catch (Exception e) {
					output.setText(output.getText() + e);
				}
			}
		});
		btnNewButton.setBounds(263, 86, 150, 23);
		frmIsharpRefactoring.getContentPane().add(btnNewButton);
	}
}
