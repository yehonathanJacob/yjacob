package Q2;

import javax.swing.*;
import javax.swing.event.AncestorEvent;
import javax.swing.event.AncestorListener;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.util.HashMap;

public class HomePanel extends JPanel {
    /**
     * instance variable
     */
    public HashMap<Q2_Date,String> data;//public, so you can handel it from outside
    private Q2_Date OldDate;
    private Q2_Date NewDate;
    private JTextArea text;

    /**
     * empty constractor
     */
    public HomePanel(){ this(new HashMap<Q2_Date,String>()); }

    /**
     * constarctor with data
     * @param Data data to read from
     */
    public HomePanel(HashMap<Q2_Date,String> Data){
        data = Data;
        OldDate = new Q2_Date();
        NewDate = new Q2_Date(OldDate);
        setLayout(new BorderLayout());


        JPanel header = new JPanel();
        header.setLayout(new FlowLayout());
        header.add(new JLabel("Date: "));
        JComboBox day = new JComboBox();
        for (int i = 1; i<=31; i++)
            day.addItem(new Item(i, i+""));
        day.setSelectedIndex(OldDate.getDay() - 1);
        day.setName("Day");
        day.addActionListener(new ComboBoxHnadler());
        header.add(day);
        header.add(new JLabel("/"));
        JComboBox month = new JComboBox();
        for (Integer id : OldDate.MonthsName.keySet())
            month.addItem(new Item(id,OldDate.MonthsName.get(id)));
        month.setSelectedIndex(OldDate.getMonth());
        month.setName("Month");
        month.addActionListener(new ComboBoxHnadler());
        header.add(month);
        header.add(new JLabel("/"));
        JComboBox year = new JComboBox();
        for (int i = OldDate.getYear() -20; i<=OldDate.getYear(); i++)
            year.addItem(new Item(i, i+""));
        year.setSelectedIndex(20);
        year.setName("Year");
        year.addActionListener(new ComboBoxHnadler());
        header.add(year);
        JButton show = new JButton("Show");
        show.addActionListener(new AbstractAction() {
            @Override
            public void actionPerformed(ActionEvent e) {
                String s1 =text.getText();
                String s2 = (data.get(OldDate) == null)? "" : data.get(OldDate);
                if(!s1.equals(s2))
                {
                    int res = JOptionPane.showConfirmDialog(null, "Would you like to save before continue?","Data is not saved over date: "+OldDate.toString(),JOptionPane.YES_NO_CANCEL_OPTION);
                    if (res == 0){
                        data.put(OldDate,text.getText());
                        OldDate = new Q2_Date(NewDate);
                        dateToData();
                    }
                    if (res == 1){
                        OldDate = new Q2_Date(NewDate);
                        dateToData();
                    }
                }
                else {
                    OldDate = new Q2_Date(NewDate);
                    dateToData();
                }
            }
        });
        header.add(show);
        add(header,BorderLayout.NORTH);

        text = new JTextArea(10,10);// where data is going to be.
        dateToData();
        add(text,BorderLayout.CENTER);

        JButton save = new JButton("save");
        save.addActionListener(new AbstractAction() {
            @Override
            public void actionPerformed(ActionEvent e) {
                data.put(OldDate,text.getText());
                JOptionPane.showMessageDialog(null, "Saved.","",JOptionPane.INFORMATION_MESSAGE);
            }
        });
        add(save,BorderLayout.SOUTH);


    }

    private class ComboBoxHnadler extends AbstractAction{
        @Override
        public void actionPerformed(ActionEvent e) {
            JComboBox c = (JComboBox) e.getSource();
            Item item = (Item) c.getSelectedItem();
            switch (c.getName()){
                case "Day":
                    NewDate.setDay(item.getId());
                    break;
                case "Month":
                    NewDate.setMonth(item.getId());
                    break;
                case "Year":
                    NewDate.setYear(item.getId());
                    break;
            }
        }
    }

    private void dateToData(){
        String s = data.get(NewDate);
        text.setText(s);
        System.out.printf("data:%s%n",s);
    }

    /**
     * class for items in ComboBox
     */
    private class Item {

        private int id;
        private String description;

        public Item(int id, String description) {
            this.id = id;
            this.description = description;
        }

        public int getId() {
            return id;
        }

        public String getDescription() {
            return description;
        }

        @Override
        public String toString() {
            return description;
        }
    }
}

