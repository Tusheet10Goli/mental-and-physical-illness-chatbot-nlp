
import { StyleSheet } from 'react-native';

import EditScreenInfo from '../components/EditScreenInfo';
import { Text, View } from '../components/Themed';

export default function AboutScreen() {
  return (
    <View style={styles.container}>
      {/* <Text style={styles.title}>About</Text>
      <View style={styles.separator} lightColor="#eee" darkColor="rgba(255,255,255,0.1)" />
      <EditScreenInfo path="/screens/AboutScreen.tsx" /> */}
       <Text style={styles.title}>
          About Our Chatbot
      </Text>
      <View style={styles.textView}>
        <Text style = {{padding:15}}>
          This app allows users to chat with an AI that predicts if they are at risk of any physical or mental illnesses. If they cannot immediately consult their healthcare providers. The feedback is just a prediction and must not be considered the offical diagnosis, prescription, or treatment. Users must consult their healthcare providers for official medical feedback and care.
        </Text>
      </View>
      <View style={styles.textView2}>
        <Text style = {{padding:15}}>
          Physical Illnesses pertain to physical health, like the flu, diabetes, hypertension, etc. {"\n"}Mental Illnesses pertain to mental helath, like anxiety, depression, etc. 
        </Text>
      </View>
      <View style={styles.textView3}>
        <Text style = {{padding:10}}>
          Log In or register to start chatting!
        </Text>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    // justifyContent: 'center',
  },
  title: {
    marginTop: 100,
    fontSize: 20,
    fontWeight: 'bold',
  },
  textView: {
    borderRadius: 30,
    borderWidth: 2, 
    borderColor: 'purple',  
    borderStyle:'solid',
    width: "70%",
    height: 210,
    marginBottom: 20,
    marginTop: 40,
    alignItems: "center",
    justifyContent: 'center'
  },
  textView2: {
    borderRadius: 30,
    borderWidth: 2, 
    borderColor: 'purple',  
    borderStyle:'solid',
    width: "70%",
    height: 130,
    marginBottom: 20,
    marginTop: 10,
    alignItems: "center",
    justifyContent: 'center'
  },
  textView3: {
    borderRadius: 15,
    borderWidth: 2, 
    borderColor: 'purple',  
    borderStyle:'solid',
    width: "70%",
    height: 60,
    marginBottom: 20,
    marginTop: 10,
    alignItems: "center",
    justifyContent: 'center'
  },
});