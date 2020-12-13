import { ReactTinyLink } from 'react-tiny-link'
import React, { useState, useEffect } from 'react';
import { 
    Row, 
    Container,
    Form,
    Spinner,
    Button 
} from 'react-bootstrap';

const Suggestion= props => {
    
    //Props
    const { suggested } = props

    // Links
    const [links, setLinks] = useState([])

    //Functions from parent
    function add_links(links){
        let values = []

        for(const link of links){
            if(link.isChecked !== 'false'){
                values.push({url: link.url})
            }
        }
        props.addLinks(values)
    }
    
    useEffect(() => {
        //Changing format of suggested links for choosing
        let urls = []
        suggested.map(e => {
            urls.push({
                isChecked: 'false',
                url: e
            })    
        });
        setLinks(urls)
    }, [suggested])
        

    const submit = e => {
        e.preventDefault()
        props.submit(false)    
    }
    const handle = index => {
        let urls = [...links]
        var checked = urls[index].isChecked
        urls[index].isChecked = checked === 'false' ? 'true' : 'false'
        setLinks([...urls])
        add_links(links)
    }
    
    return(
        <React.Fragment>
            <Container>
                <Row> 
                    <Form >
                        <Button type="submit" onClick={ e => submit(e)}>Submit</Button>
                         {links.map(

                            (link, index) => (
                                <Form.Group key={link.url} controlId="formBasicCheckbox">
                                    <Form.Check 
                                        value={link.url}
                                        type="checkbox"
                                        label="" 
                                        onChange={() => handle(index)}
                                    />
                                  <ReactTinyLink
                                        cardSize="small"
                                        showGraphic={true}
                                        maxLine={2}
                                        minLine={1}
                                        url={link.url}
                                    />
                                </Form.Group>                                                                      
                            )
                        )}
                    </Form>
                </Row>        
            </Container>
        </React.Fragment>    
    )
}
const Loading = () =>{
    return <Spinner animation="border" role="status">
                <span className="sr-only">Loading...</span>
            </Spinner> 
}
export default Suggestion;