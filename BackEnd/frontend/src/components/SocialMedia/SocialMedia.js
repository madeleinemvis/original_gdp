import Card from "react-bootstrap/Card";
import {CardDeck, Container} from "reactstrap";
import React from "react";
import TweetFreq from "./TweetFreq";
import Tweets from "./Tweets";

const Sources = props => {

    return(
        <Container className="tweets">
          <CardDeck>
              <Card>
                <Card.Body>
                    <Card.Title>Sentiment Analysis</Card.Title>
                    <Tweets uid={props.uid} />
                </Card.Body>
              </Card>
              <Card>
              <Card.Body>
                <svg width="210" height="100" viewBox="0 0 210 100">
                  <rect width="210" height="100" rx="10" ry="10" fill="#CCC" />
                </svg>
                <Card.Title>Card title that wraps to a new line</Card.Title>
                <Card.Text>
                  This is a longer card with supporting text below as a natural lead-in to
                  additional content. This content is a little bit longer.
                </Card.Text>
              </Card.Body>
            </Card>
            <Card>
              <Card.Body>
                <TweetFreq uid={props.uid}/>
              </Card.Body>
            </Card>
            <Card>
              <blockquote className="blockquote mb-0 card-body">
                <p>
                  Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer posuere
                  erat a ante.
                </p>
                <footer className="blockquote-footer">
                  <small className="text-muted">
                    Someone famous in <cite title="Source Title">Source Title</cite>
                  </small>
                </footer>
              </blockquote>
            </Card>
            <Card>
              <Card.Body>
                <svg width="210" height="100" viewBox="0 0 210 100">
                  <rect width="210" height="100" rx="10" ry="10" fill="#CCC" />
                </svg>
                <Card.Title>Card title</Card.Title>
                <Card.Text>
                  This card has supporting text below as a natural lead-in to additional
                  content.{' '}
                </Card.Text>
              </Card.Body>
              <Card.Footer>
                <small className="text-muted">Last updated 3 mins ago</small>
              </Card.Footer>
            </Card>
            <Card className="text-center, highlight-card">
              <Card.Body>
                <Card.Title>
                  Highlighted Card
                </Card.Title>
                <Card.Text>
                  Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer posuere
                  erat a ante.
                </Card.Text>
              </Card.Body>
            </Card>
            <Card className="text-center">
              <Card.Body>
                <Card.Title>Card title</Card.Title>
                <Card.Text>
                  This card has supporting text below as a natural lead-in to additional
                  content.{' '}
                </Card.Text>
                <Card.Text>
                  <small className="text-muted">Last updated 3 mins ago</small>
                </Card.Text>
              </Card.Body>
            </Card>
            <Card className="text-center, highlight-card">
              <Card.Body>
                <Card.Title>
                  Highlighted Card
                </Card.Title>
                <Card.Text>
                  Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer posuere
                  erat a ante.
                </Card.Text>
              </Card.Body>
            </Card>
            <Card>
              <Card.Body>
                <Card.Title>Card title</Card.Title>
                <Card.Text>
                  This is a wider card with supporting text below as a natural lead-in to
                  additional content. This card has even longer content than the first to
                  show that equal height action.
                </Card.Text>
                <Card.Text>
                  <small className="text-muted">Last updated 3 mins ago</small>
                </Card.Text>
              </Card.Body>
            </Card>
          </CardDeck>
    </Container>);

}

export default Sources;