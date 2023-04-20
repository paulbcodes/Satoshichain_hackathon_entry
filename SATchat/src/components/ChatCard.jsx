import React from "react";
import { Row, Card } from "react-bootstrap";
import "bootstrap/dist/css/bootstrap.min.css";
import msn from './msn.jpg';

// This is a function which renders the friends in the friends list
export function ChatCard(props) {
  return (
    <Row style={{ alignSelf: "center", marginRight: "0px" }}>
      <Card
        
        style={{ marginBottom: "2px", borderRadius: "8px", borderColor: "#d19406", width: "65%", alignSelf: "center", marginLeft: "auto", marginRight: "auto", backgroundColor: "#000000", }}
        onClick={() => {
          props.getMessages(props.publicKey);
        }}
      >
        <Card.Body >
          <Card.Title style={{ textAlign: "center" }}> {props.name} <img src={msn} alt="Logo" /></Card.Title>
          <Card.Subtitle>
          
          </Card.Subtitle>
        </Card.Body>
      </Card>
    </Row>
  );
}
