import React from "react";
import { Button, Navbar } from "react-bootstrap";

// This component renders the Navbar of our application
export function NavBar(props) {
  return (
    <Navbar style={{backgroundColor: "#000000", color: "#d19406", borderBottomWidth: "5px", borderBottomColor: "#d19406"}}>
      <Navbar.Brand href="#home" style={{backgroundColor: "#000000", color: "#d19406"}}><b>SATchat</b></Navbar.Brand>
      <Navbar.Toggle />
      <Navbar.Collapse className="justify-content-end">
        <Navbar.Text>
          <Button
            style={{ display: props.showButton }}
            variant="warning"
            onClick={async () => {
              props.login();
            }}
          >
            Connect to Metamask
          </Button>
          <div
            style={{ display: props.showButton === "none" ? "block" : "none", color: "#d19406" }}
          >
            Signed in as:
            <a href="#" style={{color: "#d19406"}}>{props.username}</a>
          </div>
        </Navbar.Text>
      </Navbar.Collapse>
    </Navbar>
  );
}
