import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * This class organizes the information of a data set into simple structures. To speed up program
 * performance, the label value of an instance is stored as an Integer that reflect the position of
 * the label in the DataSet labels list. Similarly, the attribute values of an instance are stored
 * as Integers that reflect the position of that value in the list attributes[<attribute>]. See the
 * Instance class for more details. All ordering of attribute values in an instance follow the
 * ordering of the DataSet attributes list.
 *
 * Do not modify.
 */
public class DataSet {
  public List<String> labels = null; // ordered list of class labels
  public List<String> attributes = null; // ordered list of attributes
  public Map<String, List<String>> attributeValues = null; // map to ordered discrete values taken
                                                           // by attributes
  public List<Instance> instances = null; // ordered list of instances
  private final String DELIMITER = ","; // Used to split input strings

  /**
   * Adds the labels used by the instances.
   * 
   * @param line begins with substring "%%"
   */
  public void addLabels(String line) {
    labels = new ArrayList<String>(2);

    String[] splitline = line.split(DELIMITER);
    if (splitline.length < 2) {
      System.err.println("Line doesn't contain enough labels");
      return;
    }

    // each element is a label, skip the "%%" string
    for (int i = 1; i < splitline.length; i++) {
      labels.add(splitline[i]);
    }
  }

  /**
   * Adds the attributes used by the instances.
   * 
   * @param line begins with substring "##"
   */
  public void addAttribute(String line) {
    if (attributes == null) {
      attributes = new ArrayList<String>();
      attributeValues = new HashMap<String, List<String>>();
    }

    String[] splitline = line.split(DELIMITER);
    if (splitline.length < 3) {
      System.err.println("Line doesn't contain enough attributes");
      return;
    }

    List<String> list = new ArrayList<String>();

    // grab the attribute name
    attributes.add(splitline[1]);
    attributeValues.put(splitline[1], list);

    // ordered list of values for specific attribute
    for (int i = 2; i < splitline.length; i++) {
      list.add(splitline[i]);
    }
  }

  /**
   * Add instance to collection.
   * 
   * @param line begins with label
   */
  public void addInstance(String line) {
    if (instances == null) {
      instances = new ArrayList<Instance>();
    }

    String[] splitline = line.split(DELIMITER);
    if (splitline.length < 1 + attributes.size()) { // TODO don't call .size()?
      System.err.println("Instance doesn't contain enough attributes");
      return;
    }

    Instance instance = new Instance();
    instance.label = splitline[attributes.size()];
    
    // add the values, will be input in same order as attributes
    for (int i = 0; i < splitline.length - 1; i++) {
      List<String> values = attributeValues.get(attributes.get(i));
      // find the index of the value
      for (int j = 0; j < values.size(); j++) {
        if (splitline[i].equals(values.get(j))) {
          instance.addAttribute(values.get(j));
          break;
        }
        if (j == values.size() - 1) {
          System.err.println("Missing attribute : check input files");
        }
      }
    }
    instances.add(instance);
  }

  /**
   * Verifies that two DataSets use the same values for labels and attributes as wells as the same
   * ordering. Returns false otherwise.
   */
  public boolean sameMetaValues(DataSet other) {
    // compare labels
    if (other.labels == null || this.labels == null) {
      if (!(this.labels == null && other.labels == null)) {
        return false;
      }
    } else if (other.labels.size() != this.labels.size()) {
      return false;
    } else {
      for (int i = 0; i < other.labels.size(); i++) {
        if (!other.labels.get(i).equals(this.labels.get(i))) {
          return false;
        }
      }
    }

    // compare attributes (and values)
    if (other.attributes == null || this.attributes == null) {
      if (!(this.attributes == null && this.attributes == null)) {
        return false;
      }
    } else if (other.attributes.size() != this.attributes.size()
        || other.attributes.size() != other.attributeValues.size()
        || other.attributeValues.size() != this.attributeValues.size()) {
      return false;
    } else {
      for (int i = 0; i < other.attributes.size(); i++) {
        if (!other.attributes.get(i).equals(this.attributes.get(i))) {
          return false;
        }
        List<String> otherValues = other.attributeValues.get(other.attributes.get(i));
        List<String> thisValues = this.attributeValues.get(other.attributes.get(i));
        for (int j = 0; j < otherValues.size(); j++) {
          if (!otherValues.get(j).equals(thisValues.get(j))) {
            return false;
          }
        }
      }
    }

    return true;
  }
}
