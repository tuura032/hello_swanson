'use strict';

const e = React.createElement;

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = { 
        error: null,
        isLoaded: false,
        hasVoted: false,
        items: []
    };
  }

  componentDidMount() {
    //const proxyurl = "https://cors-anywhere.herokuapp.com/";
    //const url = "https://hello-swanson.herokuapp.com/api/quote";
    const url = "http://127.0.0.1:5000/api/quote"
    fetch(url)
      .then(res => res.json())
      .then(
        (result) => {
          this.setState({
            isLoaded: true,
            items: result,
            hasVoted: false
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
    //const url = 'https://hello-swanson.herokuapp.com/api/'
    const url = "http://127.0.0.1:5000/api/";
    fetch(url + size)
      .then(res => res.json())
      .then(
        (result) => {
          this.setState({
            isLoaded: true,
            items: result ,
            hasVoted: false
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
    //fetch('https://hello-swanson.herokuapp.com/api/rating', {
    fetch('http://127.0.0.1:5000/api/rating', {
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
    this.setState({hasVoted: true});
  }
  
  render() {
    const { error, isLoaded, items, hasVoted } = this.state;
    var message;
    if (hasVoted && (items.user_rating === "Not yet rated")) {
        message = "Thank you for voting!";
    } else if (hasVoted) {
        message = "You already voted!"
    }
    if (error) {
      return <div>Error: {error.message}</div>;
    } else if (!isLoaded) {
      return <div>Loading...</div>;
    } else {
        return (
            <div className="quote-box">
                <h2>{ items.quote }</h2>
                <h4>- { items.author }</h4>
                <h5> (Word Count: {items.word_count})</h5>
                <br />
                <h3>Rating</h3>
                <h4>Average Rating: {items.average_rating} / 5</h4>
                <h4>Your Rating: {items.user_rating}</h4>
                <br />
                <h3>Click below to get a new quote!</h3>
                <button onClick={() => {this.callApi('quote')}}>
                    Random Quote
                </button>
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
                <h4>How do you like this quote? (Only 1 vote per user)</h4>
                <button onClick={() => {this.vote(1)}}>1 Star</button>
                <button onClick={() => {this.vote(2)}}>2 Stars</button>
                <button onClick={() => {this.vote(3)}}>3 Stars</button>
                <button onClick={() => {this.vote(4)}}>4 Stars</button>
                <button onClick={() => {this.vote(5)}}>5 Stars</button>
                <br />
                {message}
            </div>
            
        );
      }
    
    // if (this.state.liked) {
    //   return 'You liked this.';
    // }

    // // Display a "Like" <button>
    // return (
    //     <button onClick={() => this.setState({ liked: true })}>
    //         Get a quote!
    //     </button>
    // );
  }
}

const domContainer = document.querySelector('#app');
ReactDOM.render(e(App), domContainer);