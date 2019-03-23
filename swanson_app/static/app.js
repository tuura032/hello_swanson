'use strict';

const e = React.createElement;

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = { 
        error: null,
        isLoaded: false,
        displayVoteMessage: false,
        items: []
    };
  }

  componentDidMount() {
    //const proxyurl = "https://cors-anywhere.herokuapp.com/";
    const url = "https://hello-swanson.herokuapp.com/api/quote";
    //const url = "http://127.0.0.1:5000/api/quote"
    fetch(url)
      .then(res => res.json())
      .then(
        (result) => {
          this.setState({
            isLoaded: true,
            items: result
          });
        },
        (error) => {
          this.setState({
            isLoaded: true,
            error
          });
        }
      )
  }

  callApi(size) {
    const url = 'https://hello-swanson.herokuapp.com/api/'
    //const url = "http://127.0.0.1:5000/api/";
    fetch(url + size)
      .then(res => res.json())
      .then(
        (result) => {
          this.setState({
            isLoaded: true,
            items: result,
            displayVoteMessage: false
          });
        },
        (error) => {
          this.setState({
            isLoaded: true,
            error
          });
        }
      )
  }

  vote(rating) {
    if (this.state.items.has_voted) {
        console.log("api not called, already rated");
    } else {
    
        fetch('https://hello-swanson.herokuapp.com/api/rating', {
        //fetch('http://127.0.0.1:5000/api/rating', {
            method: 'POST',
            headers: {
            Accept: 'application/json',
            'Content-Type': 'application/json',
            },
            body: JSON.stringify({
            user_rating: rating,
            quote_id: this.state.items.id
            })
        });
    }
    this.setState({displayVoteMessage: true});
  }
  
  render() {
    // get state items
    const { error, isLoaded, items } = this.state;
    
    // determine message to display when clicking on vote
    var message;
    if (this.state.displayVoteMessage && (!items.has_voted)) {
         message = "Thank you for voting!";
    } else if (items.has_voted) {
         message = "You already voted!"
    } else {
         message = ""
    }

    // return content
    if (error) {
      return <div>Error: {error.message}</div>;
    } else if (!isLoaded) {
      return <div>Loading...</div>;
    } else if (items.has_voted) {
        return (
            <div className="quote-box">
                <h2>{ items.quote }</h2>
                <h4>- { items.author }</h4>
                <h5> (Word Count: {items.word_count})</h5>
                <br />
                <h3>Click below to get a new quote!</h3>
                <button onClick={() => {this.callApi('quote')}}>
                    Random Quote
                </button>
                <br />
                <button onClick={() => {this.callApi('large')}}>
                Big Quote
                </button>
                <button onClick={() => {this.callApi('medium')}}>
                Medium Quote
                </button>
                <button onClick={() => {this.callApi('small')}}>
                Small Quote
                </button>
                <br /><br />
                <br />
                <h4>Average Rating: {items.average_rating} / 5</h4>
                <h4>Your Rating: {items.user_rating}</h4>
                <br />
            </div>
        )
    } else {
        return (
            <div className="quote-box">
                <h2>{ items.quote }</h2>
                <h4>- { items.author }</h4>
                <h5> (Word Count: {items.word_count})</h5>
                <br />
                <h3>Click below to get a new quote!</h3>
                <button onClick={() => {this.callApi('quote')}}>
                    Random Quote
                </button>
                <br />
                <button onClick={() => {this.callApi('large')}}>
                Big Quote
                </button>
                <button onClick={() => {this.callApi('medium')}}>
                Medium Quote
                </button>
                <button onClick={() => {this.callApi('small')}}>
                Small Quote
                </button>
                <br /><br />
                {message}
                <br />
                <br />
                <h3>Rating</h3>
                <h4>How do you like this quote? (Only 1 vote per user)</h4>
                <button onClick={() => {this.vote(1)}}>1 Star</button>
                <button onClick={() => {this.vote(2)}}>2 Stars</button>
                <button onClick={() => {this.vote(3)}}>3 Stars</button>
                <button onClick={() => {this.vote(4)}}>4 Stars</button>
                <button onClick={() => {this.vote(5)}}>5 Stars</button>
                <br />                
                <br />
                <h4>Average Rating: {items.average_rating} / 5</h4>
                <h4>Your Rating: {items.user_rating}</h4>
                <br />
            </div>
            
        );
      }
  }
}

const domContainer = document.querySelector('#app');
ReactDOM.render(e(App), domContainer);