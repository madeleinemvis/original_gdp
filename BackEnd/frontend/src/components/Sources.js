import Card from "react-bootstrap/Card";
import WordCloud from "./WordCloud";
import {CardColumns, Container} from "reactstrap";
import React from "react";

const Sources = () => {

    return(<Container>
        <CardColumns>
            <Card style={{ width: '22rem' }}>
              <Card.Body>
                  <Card.Title>Word Cloud</Card.Title>
                  <WordCloud />
              </Card.Body>
            </Card>
        </CardColumns>

    </Container>);

}

export default Sources;