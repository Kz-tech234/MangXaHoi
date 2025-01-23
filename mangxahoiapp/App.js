import { StatusBar } from 'expo-status-bar';
import { StyleSheet, Text, View } from 'react-native';

import { getDatabase, ref, set } from "firebase/database";

// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyBA71OL95JtgK6ryUbXqQvGDsTSf9ZMCQg",
  authDomain: "mangxahoi-44414.firebaseapp.com",
  databaseURL: "https://mangxahoi-44414-default-rtdb.firebaseio.com",
  projectId: "mangxahoi-44414",
  storageBucket: "mangxahoi-44414.firebasestorage.app",
  messagingSenderId: "688491545111",
  appId: "1:688491545111:web:59b8be7ba851d251f45252",
  measurementId: "G-6R473S2128"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);


function guiDuLieu() {
  const db = getDatabase();
  set(ref(db, 'Dia chi gui len'), {
    tenBien: "gia tri gui len"  });
}


export default function App() {
  return (
    <View style={styles.container}>
      <Text>Open up App.js to start working on your app!</Text>
      <StatusBar style="auto" />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
  },
});
