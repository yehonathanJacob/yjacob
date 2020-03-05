import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.*;
import java.lang.Math;

/**
 * Fill in the implementation details of the class DecisionTree using this file. Any methods or
 * secondary classes that you want are fine but we will only interact with those methods in the
 * DecisionTree framework.
 *
 * You must add code for the 1 member and 4 methods specified below.
 *
 * See DecisionTree for a description of default methods.
 */
public class DecisionTreeImpl extends DecisionTree {
  private DecTreeNode root;
  //ordered list of class labels
  private List<String> labels;
  //ordered list of attributes
  private List<String> attributes;
  //map to ordered discrete values taken by attributes
  private Map<String, List<String>> attributeValues;

  /**
   * Answers static questions about decision trees.
   */
  DecisionTreeImpl() {
    // no code necessary this is void purposefully
  }

  /**
   * Build a decision tree given only a training set.
   *
   * @param train: the training set
   */
  DecisionTreeImpl(DataSet train) {

    this.labels = train.labels;
    this.attributes = train.attributes;
    this.attributeValues = train.attributeValues;
    // TODO: add code here
    String rootDefaultLabel = priorityLable(train.instances, null);
    this.root = treeForChild(train.instances, attributes, rootDefaultLabel, null);
  }

  /**
   * @param instances of DataSet
   * @param attributes of table
   * @param defaultLabel - the priority one
   * @param parentAttributeValue - the value of the parent
   * @return Node ot a tree
   */
  DecTreeNode treeForChild(List<Instance> instances, List<String> attributes, String defaultLabel, String parentAttributeValue) {
      DecTreeNode node = null;
      // check if we are in leaf
      if (   instances.isEmpty() // no more data to train
          || checkEqualsLables(instances) // all instances has same lables (so they are equal)
          || attributes.isEmpty()
         )
          return node = new DecTreeNode(priorityLable(instances,defaultLabel), "", parentAttributeValue, true);

      // find best attribute to go next
      double highestGainScore = -1,Gain_A;
      String bestAttribute = null,attr;
      int bestAttribute_i = -1;
      for (int attr_i =0;attr_i<attributes.size(); attr_i++){
          attr = attributes.get(attr_i);
          // calc Gain(A) (Pg. 704)
          Gain_A = entropy(instances) - Remainder_A(instances,attr);

          if(Gain_A>highestGainScore){
              highestGainScore = Gain_A;
              bestAttribute = attr;
              bestAttribute_i = attr_i;
          }
      }

      node = new DecTreeNode(priorityLable(instances,defaultLabel), bestAttribute, parentAttributeValue, false);

      List<String> leftAttributes = new ArrayList<String>(attributes);
      leftAttributes.remove(bestAttribute_i);
      double d; // d is number of values of attr (Pg. 704)
      d= attributeValues.get(bestAttribute).size();
      HashMap<String,List<Instance>> valueOfAttrToInst =  new HashMap<String,List<Instance>>();
      String value;
      List<Instance> instList;
      for (int i = 0; i < instances.size(); i++){
          value = instances.get(i).attributes.get(getAttributeIndex(bestAttribute));
          if (!valueOfAttrToInst.containsKey(value)){
              instList = new ArrayList<Instance>();
              valueOfAttrToInst.put(value,instList);
          }

          valueOfAttrToInst.get(value).add(instances.get(i));
      }

      for (int value_i =0;value_i<d;value_i++){
          value =attributeValues.get(bestAttribute).get(value_i);
          if (valueOfAttrToInst.containsKey(value)) {
              instList = valueOfAttrToInst.get(value);
          }else {
              instList = new ArrayList<Instance>();
          }
              DecTreeNode child = treeForChild(instList, leftAttributes, priorityLable(instances,defaultLabel), value);
              node.addChild(child);

      }

      return node;
  }

  /**
   * @param instances
   * @return True if all lables are the same. False otherwise.
   */
  boolean checkEqualsLables(List<Instance> instances) {
    if (instances.isEmpty())
      return true;
    String firstLable = instances.get(0).label;
    for (int i = 1; i< instances.size();i++){
      if (!instances.get(i).label.equals(firstLable))
        return false;
    }
    return true;
  }

  /**
   * @param instances
   * @return the priority lable in from instances list
   */
  String priorityLable(List<Instance> instances,String defaultLabel){
    HashMap<String,Integer> lablesToNum =  new HashMap<String,Integer>();
    for(int i=0; i < labels.size();i++)
      lablesToNum.put(labels.get(i),0);
    int temp,maxLableNum = -1;
    String lable,maxLable = defaultLabel;
    for (int i =0; i< instances.size();i++){
      lable = instances.get(i).label;
      temp = lablesToNum.get(lable);
      temp +=1;
      lablesToNum.put(lable,temp);
      if (maxLableNum < temp)
        maxLable = lable;
    }
    return maxLable;
  }

    /**
     * @param instances - training data
     * @return the H(Goal) of the entropy
     */
  double entropy(List<Instance> instances) {
      HashMap<String,Double> lablesToRate =  new HashMap<String,Double>();
      for(int i=0; i < labels.size();i++)
          lablesToRate.put(labels.get(i),0.0);
      double temp, totalData = instances.size();
      String lable;
      // calc the rate of each lable
      for (int i =0; i< totalData;i++){
          lable = instances.get(i).label;
          temp = lablesToRate.get(lable);
          temp +=1.0;
          lablesToRate.put(lable,temp);
      }
      // sum the data rate with the function of the entropy
      double rate,H_V = 0.0;
      for (int j =0;j<labels.size();j++ ){
          if(lablesToRate.containsKey(labels.get(j))){
              rate = lablesToRate.get(labels.get(j))/((double)totalData);
              H_V += (-1.0)*rate*(Math.log(rate)/Math.log(2));
          }
      }
      return H_V;
      // return entropyValue
  }

    /**
     * @param instances - the total train data
     * @param attr - to chek the data remainder
     * @return the Remainder(A)
     */
  double Remainder_A(List<Instance> instances, String attr) {
      int totalData = instances.size();
      int d = attributeValues.get(attr).size(); // d is number of values of attr (Pg. 704)
      int attr_i = getAttributeIndex(attr);
      HashMap<String,Double> valueToSum =  new HashMap<String,Double>();
      HashMap<String,List<Integer>> lablesToValuesRate =  new HashMap<String,List<Integer>>();
      String value_name, lable;
      double temp;
      int value_i;
      List<Integer> valuesSumList;
      for (value_i = 0; value_i < d; value_i++) {
          value_name = attributeValues.get(attr).get(value_i);
          valueToSum.put(value_name, 0.0);
      }
      for(int i=0; i < labels.size();i++) {
          valuesSumList = new ArrayList<Integer>();
          for (value_i = 0; value_i < d; value_i++)
              valuesSumList.add(0);
          lablesToValuesRate.put(labels.get(i), valuesSumList);
      }

      for (int i = 0; i < totalData; i++){
          value_name = instances.get(i).attributes.get(attr_i);
          temp = valueToSum.get(value_name);
          temp += 1;
          valueToSum.put(value_name, temp);
          lable = instances.get(i).label;
          valuesSumList = lablesToValuesRate.get(lable);
          temp = valuesSumList.get(getAttributeValueIndex(attr,value_name));
          temp +=1.0;
          valuesSumList.set(getAttributeValueIndex(attr,value_name),(int)temp);
          lablesToValuesRate.put(lable,valuesSumList);
      }

      double sigmaSum = 0.0,value_sum,lable_value_sum,B,rate,totalValueRate;
      for (value_i = 0; value_i < d; value_i++){
          value_name = attributeValues.get(attr).get(value_i);
          value_sum = valueToSum.get(value_name);
          B = 0;
          for (int label_i = 0;label_i<labels.size();label_i++){
              valuesSumList = lablesToValuesRate.get(labels.get(label_i));
              lable_value_sum = valuesSumList.get(getAttributeValueIndex(attr,value_name));
              if (lable_value_sum>0) {
                  rate = lable_value_sum / value_sum;
                  B += (-1.0) * rate * (Math.log(rate) / Math.log(2));
              }
          }
          totalValueRate = value_sum/((double)totalData);
          sigmaSum+= totalValueRate*B;

      }
      return sigmaSum;
  }

    /**
     * @param instance to test
     * @return label from tree
     */
  @Override
  public String classify(Instance instance) {
	  DecTreeNode node = root;
	  while(!node.terminal) {
		  for (int i = 0; i < node.children.size(); i++)
			  if(instance.attributes.get(getAttributeIndex(node.attribute)).equals(node.children.get(i).parentAttributeValue)) {
				  node = node.children.get(i);
				  break;
			  }
	  }
	  return node.label;
  }

    /**
     * @param train - DataSet
     * print to stdout the train tree
     */
  @Override
  public void rootInfoGain(DataSet train) {
    this.labels = train.labels;
    this.attributes = train.attributes;
    this.attributeValues = train.attributeValues;
    double entropy_val,Remainder_A_val,Gain_A_val;
      for (int i = 0; i < train.attributes.size(); i++) {
          entropy_val = entropy(train.instances);
          Remainder_A_val = Remainder_A(train.instances, train.attributes.get(i));
          Gain_A_val = entropy_val - Remainder_A_val;
          System.out.format("%s %.5f\n", train.attributes.get(i), Gain_A_val);
      }
  }

  @Override
  public void printAccuracy(DataSet test) {
    int correct, total;
    total = test.instances.size();
    correct = 0;
    for (int inst_i = 0; inst_i < total; inst_i ++){
        if (test.instances.get(inst_i).label.equals(classify(test.instances.get(inst_i))))
            correct+=1;
    }
    double result = (double)correct/total;
    System.out.format("%.4f\n", result);
  }
    /**
   * Build a decision tree given a training set then prune it using a tuning set.
   * ONLY for extra credits
   * @param train: the training set
   * @param tune: the tuning set
   */
  DecisionTreeImpl(DataSet train, DataSet tune) {

    this.labels = train.labels;
    this.attributes = train.attributes;
    this.attributeValues = train.attributeValues;
    // TODO: add code here
    // only for extra credits
  }

  @Override
  /**
   * Print the decision tree in the specified format
   */
  public void print() {

    printTreeNode(root, null, 0);
  }

  /**
   * Prints the subtree of the node with each line prefixed by 4 * k spaces.
   */
  public void printTreeNode(DecTreeNode p, DecTreeNode parent, int k) {
    StringBuilder sb = new StringBuilder();
    for (int i = 0; i < k; i++) {
      sb.append("    ");
    }
    String value;
    if (parent == null) {
      value = "ROOT";
    } else {
      int attributeValueIndex = this.getAttributeValueIndex(parent.attribute, p.parentAttributeValue);
      value = attributeValues.get(parent.attribute).get(attributeValueIndex);
    }
    sb.append(value);
    if (p.terminal) {
      sb.append(" (" + p.label + ")");
      System.out.println(sb.toString());
    } else {
      sb.append(" {" + p.attribute + "?}");
      System.out.println(sb.toString());
      for (DecTreeNode child : p.children) {
        printTreeNode(child, p, k + 1);
      }
    }
  }

  /**
   * Helper function to get the index of the label in labels list
   */
  private int getLabelIndex(String label) {
    for (int i = 0; i < this.labels.size(); i++) {
      if (label.equals(this.labels.get(i))) {
        return i;
      }
    }
    return -1;
  }

  /**
   * Helper function to get the index of the attribute in attributes list
   */
  private int getAttributeIndex(String attr) {
    for (int i = 0; i < this.attributes.size(); i++) {
      if (attr.equals(this.attributes.get(i))) {
        return i;
      }
    }
    return -1;
  }

  /**
   * Helper function to get the index of the attributeValue in the list for the attribute key in the attributeValues map
   */
  private int getAttributeValueIndex(String attr, String value) {
    for (int i = 0; i < attributeValues.get(attr).size(); i++) {
      if (value.equals(attributeValues.get(attr).get(i))) {
        return i;
      }
    }
    return -1;
  }
}
